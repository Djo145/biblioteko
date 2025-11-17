```mermaid
classDiagram
    %% Class Diagram: Rent a Copyrighted Work

    class Rental {
      +UUID rentalId
      +UUID userId
      +UUID workId
      +Date startedAt
      +Date expiresAt
      +String status  %% refers to RentalStatus
    }

    class EncryptionKey {
      +UUID keyId
      +String encryptedKeyBlob
      +String algorithm
    }

    class StorageRecord {
      +String storagePath
      +Date storedAt
      +String accessControl
    }

    %% Represent the enumeration as a simple class
    class RentalStatus {
      +Active
      +Expired
      +Revoked
    }

    class User {
      +UUID userId
      +String displayName
    }

    class Work {
      +UUID workId
      +String title
    }

    %% Relationships
    Rental "1" -- "1" EncryptionKey
    Rental "1" -- "1" StorageRecord
    User "1" -- "0..*" Rental
    Work "1" -- "0..*" Rental

    ```
