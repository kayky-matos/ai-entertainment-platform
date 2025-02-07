```mermaid

graph TB
    subgraph Data Collection Layer
        WS[Web Scraping Engine]
        SM[Social Media APIs]
        IMG[Image Collector]
    end

    subgraph Storage Layer
        VDB[(Vector Database)]
        RDB[(Relational Database)]
        ML[(Media Library)]
    end

    subgraph Processing Layer
        subgraph Content Processing
            SA[Sentiment Analysis]
            CF[Content Filtering]
            TC[Text Classification]
            IC[Image Classification]
        end

        subgraph AI Models
            DNN[Deep Neural Networks]
            TM[Transformer Models]
            VS[Vector Search]
        end
    end

    subgraph Application Layer
        RC[Recommendation Engine]
        RAG[RAG Chatbot]
        UI[User Interface]
        API[API Gateway]
    end

    subgraph External Systems
        ST[Streaming Platforms]
        SMP[Social Media Platforms]
        ED[Entertainment Databases]
    end

    %% Data Collection Flow
    ED --> WS
    SMP --> SM
    ED --> IMG

    %% Storage Flow
    WS --> RDB
    SM --> RDB
    IMG --> ML

    %% Processing Flow
    RDB --> SA
    RDB --> CF
    RDB --> TC
    ML --> IC

    %% AI Model Integration
    SA --> DNN
    TC --> TM
    IC --> VS

    %% Vector Database Population
    DNN --> VDB
    TM --> VDB
    VS --> VDB

    %% Application Layer Integration
    VDB --> RC
    VDB --> RAG
    RDB --> API
    ML --> API

    %% User Interface Integration
    RC --> UI
    RAG --> UI
    API --> UI

    %% External Integration
    ST --> API

    %% Styling
    classDef storage fill:#f9f,stroke:#333,stroke-width:2px
    classDef processing fill:#bbf,stroke:#333,stroke-width:2px
    classDef external fill:#fbb,stroke:#333,stroke-width:2px
    classDef application fill:#bfb,stroke:#333,stroke-width:2px

    class VDB,RDB,ML storage
    class SA,CF,TC,IC,DNN,TM,VS processing
    class ST,SMP,ED external
    class RC,RAG,UI,API application
