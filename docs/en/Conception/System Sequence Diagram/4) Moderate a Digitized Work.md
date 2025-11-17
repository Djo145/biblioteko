```mermaid
sequenceDiagram
    participant Librarian
    participant Application
    participant NL_France_Server as "National Library Server"

    Note over Application,NL_France_Server: Prerequisite: a submitted file awaits moderation

    Librarian->>Application: Log in
    Application->>NL_France_Server: Authenticate librarian (credentials)
    NL_France_Server-->>Application: Auth result
    Application-->>Librarian: Show dashboard / submitted works list

    Librarian->>Application: Set filters (e.g., language, format, date, tags)
    Application->>NL_France_Server: Query submitted works with filters
    NL_France_Server-->>Application: Return filtered list
    Application-->>Librarian: Display filtered results

    Librarian->>Application: Set sorting criteria (e.g., newest, priority)
    Application-->>NL_France_Server: Request sorted results or sort client-side
    NL_France_Server-->>Application: Return sorted results
    Application-->>Librarian: Display sorted list

    Librarian->>Application: Select a file for a work
    Application->>NL_France_Server: Fetch metadata and file location
    NL_France_Server-->>Application: Return metadata + file (or storage pointer)
    Application-->>Librarian: Display submitter info
    Application-->>Librarian: Open reader/viewer (appropriate to file type)

    Librarian->>Application: Review work (read pages, inspect scans, check OCR)
    Note right of Librarian: Review may include zoom, page-by-page, OCR text

    Librarian->>Application: Complete/augment work information (catalog fields)
    Application->>NL_France_Server: Save updated metadata
    NL_France_Server-->>Application: Confirm save

    Librarian->>Application: Accept work and specify nature (e.g., public-domain, restricted, needs redaction)
    Application->>NL_France_Server: Update work status = accepted; store nature & access rules
    NL_France_Server-->>Application: Confirmation + updated status
    Application-->>Librarian: Show success / next steps

    Note over NL_France_Server,Application: If rejected/flagged -> notify submitter / route to admin workflow

    
```
