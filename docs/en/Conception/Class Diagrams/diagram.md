```mermaid
classDiagram
    %% =========================
    %% MAIN ACTORS
    %% =========================
    class User {
        +id
        +name
        +publicKey
        +privateKey
        +authenticate()
        +consultWork()
    }
    class Member {
        +depositWork()
        +rentWork()
    }
    class Librarian {
        +moderateWork()
        +modifyMetadata()
        +validatePublicDomain()
    }
    User <|-- Member
    Member <|-- Librarian
    %% =========================
    %% BUSINESS ENTITIES
    %% =========================
    class Work {
        +id
        +title
        +author
        +type
        +category
        +rightsStatus
        +file
        +metadata
    }
    class GitRepository {
        +addWork()
        +commit()
        +listWorks() 
        +modifyMetadata()
    }
    class AI_OCR {
        +extractText(pdf)
        +convertMarkdown()
    }
    class System {
        +verifyRights()
        +distributeOpenWork()
        +scheduleTasks()
    }
    class Authentication {
        +franceConnectLogin()
        +createLocalIdentifier()
        +generateToken()
    }
    class Notification {
        +sendNotification()
        +synchronizeMembers()
    }
    %% =========================
    %% CLASS RELATIONSHIPS
    %% =========================
    User --> Authentication : connects via
    Member --> GitRepository : deposits a work
    Librarian --> GitRepository : moderates and validates
    Work --> GitRepository : is stored in
    Librarian --> Work : modifies / validates
    Member --> Work : creates / consults
    System --> Work : updates rights
    System --> Notification : informs members
    AI_OCR --> Work : extracts text
    GitRepository --> Work : versions
    Notification --> User : alerts
    %% =========================
    %% LINK WITH SCENARIOS
    %% =========================
    class SC_InstallApp {
        <<Scenario>>
    }
    class SC_BecomeMember {
        <<Scenario>>
    }
    class SC_Connect {
        <<Scenario>>
    }
    class SC_BecomeLibrarian {
        <<Scenario>>
    }
    class SC_DepositWork {
        <<Scenario>>
    }
    class SC_ModerateWork {
        <<Scenario>>
    }
    class SC_OCR {
        <<Scenario>>
    }
    class SC_RentWork {
        <<Scenario>>
    }
    class SC_PublicDomainTransition {
        <<Scenario>>
    }
    class SC_OpenDistribution {
        <<Scenario>>
    }
    %% Associations between scenarios and classes
    SC_InstallApp --> User
    SC_BecomeMember --> Authentication
    SC_Connect --> Authentication
    SC_BecomeLibrarian --> Librarian
    SC_DepositWork --> Member
    SC_DepositWork --> GitRepository
    SC_ModerateWork --> Librarian
    SC_ModerateWork --> GitRepository
    SC_OCR --> AI_OCR
    SC_OCR --> Work
    SC_RentWork --> Member
    SC_RentWork --> Work
    SC_RentWork --> System
    SC_PublicDomainTransition --> System
    SC_PublicDomainTransition --> Librarian
    SC_OpenDistribution --> System
    SC_OpenDistribution --> Notification
    ```
