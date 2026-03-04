# Clean Architecture Standards

This project follows Clean Architecture principles with clear separation of concerns across layers. Follow these standards strictly when adding or modifying code.

## Project Structure

```
be/
├── domain/          # Enterprise business rules (innermost layer)
├── application/     # Application business rules
├── infrastructure/  # Framework & drivers (outermost layer)
├── interface/       # Controllers, schemas, dependencies
└── shared/          # Cross-cutting concerns (config, database)
```

## Layer Responsibilities & Dependencies

### 1. Domain Layer (`domain/entities/`)
**Purpose**: Pure business entities with business logic and validation

**Rules**:
- Contains ONLY pure Python classes with NO external dependencies
- NO imports from other layers (application, infrastructure, interface, shared)
- NO framework dependencies (FastAPI, SQLAlchemy, etc.)
- Implement validation logic in `__init__` methods
- Raise `ValueError` for business rule violations

**Example**:
```python
class User:
    def __init__(self, id, email, name, phone, password):
        if "@" not in email:
            raise ValueError("E-mail is missing @")
        self.id = id
        self.email = email
        self.name = name
        self.phone = phone
        self.password = password
```

### 2. Application Layer (`application/`)

#### 2.1 Ports (`application/ports/`)
**Purpose**: Define interfaces/contracts for external dependencies

**Rules**:
- Use `Protocol` from typing for interface definitions
- Define method signatures without implementation
- Import ONLY from `domain/` layer
- Name interfaces clearly (e.g., `UserRepository`, `PasswordHashing`, `TokenHandler`)

**Example**:
```python
from typing import Protocol
from domain.entities.user import User

class UserRepository(Protocol):
    def __init__(self, db) -> None: ...
    def create_user(self, user: User) -> None: ...
    def user_exists(self, email: str) -> bool: ...
    def get_user_by_email(self, email: str) -> User | None: ...
```

#### 2.2 Use Cases (`application/use_cases/`)
**Purpose**: Orchestrate business logic and coordinate between domain and ports

**Rules**:
- Each use case is a class with an `execute()` method
- Inject dependencies via `__init__` (use Port interfaces, NOT concrete implementations)
- Import from `domain/` and `application/ports/` ONLY
- NO imports from `infrastructure/` or `interface/`
- Return domain entities, NOT framework-specific objects
- Raise `ValueError` for application errors
- Use descriptive class names ending in action verbs (e.g., `RegisterUser`, `SignIn`, `RetrieveUser`)

**Example**:
```python
from application.ports import UserRepository, PasswordHashing
from domain.entities.user import User

class RegisterUser:
    def __init__(self, user_repo: UserRepository, password_hashing: PasswordHashing) -> None:
        self.user_repo = user_repo
        self.password_hashing = password_hashing

    def execute(self, email: str, name: str, phone: str, password: str):
        if self.user_repo.user_exists(email):
            raise ValueError("An user already exists with this email")
        
        hashed_password = self.password_hashing.get_password_hash(password)
        new_user = User(id=None, email=email, name=name, phone=phone, password=hashed_password)
        
        try:
            self.user_repo.create_user(new_user)
        except Exception as e:
            raise ValueError("Error while creating a new account.")
        
        return new_user
```

### 3. Infrastructure Layer (`infrastructure/`)

#### 3.1 Models (`infrastructure/models/`)
**Purpose**: ORM models for database persistence

**Rules**:
- Use SQLAlchemy ORM models
- Import from `shared.database` for Base class
- Define `to_domain()` method to convert to domain entities
- Use proper column types and constraints
- Include relationships with cascade options
- Include timestamp fields (`created_at`, `updated_at`)
- Avoid importing from pending models using placeholder approach

**Example**:
```python
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from shared.database import Base
from domain.entities import User as UserDomain

# Avoid circular imports
Asset, Client, Company = [None, None, None]

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = mapped_column(String, unique=True, index=True, nullable=False)
    # ... other fields
    
    assets: Mapped[list["Asset"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    
    def to_domain(self):
        return UserDomain(id=self.id, email=self.email, ...)
```

#### 3.2 Repositories (`infrastructure/repositories/`)
**Purpose**: Implement port interfaces with concrete database logic

**Rules**:
- Implement Port protocols from `application/ports/`
- Import concrete Port as alias: `from application.ports import UserRepository as UserRepositoryContract`
- Use SQLAlchemy Session for database operations
- Convert between ORM models and domain entities
- Use domain entities in method signatures, NOT ORM models
- Handle database sessions via dependency injection

**Example**:
```python
from sqlalchemy.orm import Session
from domain.entities.user import User
from application.ports import UserRepository as UserRepositoryContract
from infrastructure.models.user import User as UserModel

class UserRepository(UserRepositoryContract):
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_user(self, user: User) -> None:
        new_user = UserModel(email=user.email, name=user.name, ...)
        self.db.add(new_user)
        self.db.commit()
```

#### 3.3 Security (`infrastructure/security/`)
**Purpose**: Implement security-related ports (password hashing, token handling)

**Rules**:
- Implement Port protocols from `application/ports/`
- Use appropriate libraries (passlib, jose, etc.)
- No business logic, only technical implementation

### 4. Interface Layer (`interface/`)

#### 4.1 Controllers (`interface/controllers/`)
**Purpose**: HTTP endpoint handlers

**Rules**:
- Use FastAPI routers
- Inject use cases via `Depends()` from dependency functions
- Handle serialization between schemas and domain entities
- Convert use case errors to HTTP exceptions
- Keep controllers thin - delegate to use cases
- Type hint dependencies with `Annotated[UseCase, Depends(dependency_function)]`

**Example**:
```python
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from interface.deps import register_use_case
from interface.schemas import UserCreate, UserResponse
from application.use_cases import RegisterUser

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(
    user_data: UserCreate,
    use_case: Annotated[RegisterUser, Depends(register_use_case)],
):
    try:
        user = use_case.execute(email=user_data.email, ...)
        return UserResponse(id=str(user.id), email=user.email, ...)
    except ValueError as e:
        raise HTTPException(400, str(e))
```

#### 4.2 Dependencies (`interface/deps/`)
**Purpose**: FastAPI dependency injection setup

**Rules**:
- Create factory functions that return use case instances
- Inject all dependencies (repositories, security services)
- Wire concrete implementations to ports
- Use FastAPI `Depends()` for dependency chain

**Example**:
```python
from fastapi import Depends
from typing import Annotated
from application.use_cases import RegisterUser
from infrastructure.repositories.user import UserRepository
from infrastructure.security.password_hashing import PasswordHashing

def register_use_case(
    password_hashing: Annotated[PasswordHashing, Depends(get_password_hashing)],
    user_repository: Annotated[UserRepository, Depends(get_user_repo)],
):
    return RegisterUser(user_repo=user_repository, password_hashing=password_hashing)
```

#### 4.3 Schemas (`interface/schemas/`)
**Purpose**: Pydantic models for request/response validation

**Rules**:
- Use Pydantic models
- Separate schemas for requests and responses
- NO business logic in schemas

### 5. Shared Layer (`shared/`)
**Purpose**: Cross-cutting concerns

**Rules**:
- Configuration management (`config.py`)
- Database setup (`database.py` with Base, engine, SessionLocal)
- Can be imported by any layer when needed
- Keep minimal and focused on infrastructure concerns

## Dependency Rules (Critical)

**Dependency direction MUST flow inward**:
```
interface → application → domain
     ↓           ↓
infrastructure (implements ports)
```

**Allowed imports by layer**:
- `domain/`: NO external layer imports
- `application/ports/`: domain only
- `application/use_cases/`: domain + application/ports only
- `infrastructure/`: domain + application/ports + shared
- `interface/`: all layers
- `shared/`: framework dependencies only

**FORBIDDEN**:
- Domain importing from application/infrastructure/interface
- Application importing from infrastructure/interface
- Use cases directly importing repositories or security implementations

## Naming Conventions

- **Domain entities**: Singular nouns (e.g., `User`, `Company`, `Asset`)
- **Use cases**: Action verbs (e.g., `RegisterUser`, `SignIn`, `RetrieveUser`)
- **Repositories**: `<Entity>Repository` (e.g., `UserRepository`)
- **Ports**: Interface name (e.g., `UserRepository`, `PasswordHashing`)
- **Controllers**: REST verb + entity (e.g., `def register()`, `def login()`)
- **Dependency functions**: `get_<component>` (e.g., `get_user_repo`, `register_use_case`)

## Error Handling

- Domain layer: Raise `ValueError` for business rule violations
- Application layer: Raise `ValueError` for application errors
- Infrastructure layer: Let exceptions propagate or wrap in `ValueError`
- Interface layer: Convert exceptions to `HTTPException` with appropriate status codes

## Testing Strategy (Future)

- Test domain entities independently
- Test use cases with mocked ports
- Test repositories with test database
- Test controllers with mocked use cases
