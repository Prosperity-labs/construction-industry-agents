# Dependency Graph - Construction Industry Agents

## System Component Dependencies

```mermaid
graph TD
    %% Main Entry Points
    A[demo_system.py] --> B[workflow_orchestrator.py]
    A --> C[system_builder.py]
    
    %% Core Workflow Orchestrator Dependencies
    B --> D[excel_parser_agent.py]
    B --> E[supplier_mapping_agent.py]
    B --> F[communication_agent.py]
    B --> G[response_parser_agent.py]
    B --> H[quote_calculator_agent.py]
    B --> I[document_generator_agent.py]
    
    %% System Builder Dependencies
    C --> J[diagrams/complete_system_architecture.mmd]
    C --> K[diagrams/agent_workflow&data_flow.mmd]
    C --> D
    C --> E
    C --> F
    C --> G
    C --> H
    C --> I
    
    %% Agent Internal Dependencies
    D --> L[openai]
    D --> M[pandas]
    D --> N[openpyxl]
    D --> O[dataclasses]
    
    E --> P[dataclasses]
    E --> Q[json]
    E --> R[pathlib]
    
    F --> S[requests]
    F --> T[email]
    F --> U[dataclasses]
    F --> E
    
    G --> V[re]
    G --> W[json]
    G --> X[dataclasses]
    G --> F
    
    H --> Y[dataclasses]
    H --> Z[math]
    H --> AA[json]
    H --> G
    
    I --> BB[openpyxl]
    I --> CC[pandas]
    I --> DD[dataclasses]
    I --> H
    
    %% Testing Dependencies
    AB[test_suite.py] --> B
    AB --> D
    AB --> E
    AB --> F
    AB --> G
    AB --> H
    AB --> I
    
    AC[test_runner.py] --> AB
    AC --> AD[tests/input/]
    AC --> AE[tests/output/]
    
    %% Visual Components
    AF[simple_visual_demo.py] --> B
    AG[visual_workflow_monitor.py] --> B
    
    %% Data Dependencies
    AH[test_construction_spec.xlsx] --> D
    AI[demo_response.json] --> G
    
    %% Output Dependencies
    AJ[complete_workflow_output/] --> I
    AK[demo_output/] --> I
    AL[visual_workflow_output/] --> I
    
    %% Configuration Dependencies
    AM[requirements.txt] --> L
    AM --> M
    AM --> N
    AM --> S
    
    %% Documentation Dependencies
    AN[README.md] --> AO[diagrams/]
    AP[licence.md] --> AN
    
    %% Styling
    classDef entryPoint fill:#e1f5fe
    classDef coreAgent fill:#f3e5f5
    classDef dependency fill:#e8f5e8
    classDef test fill:#fff3e0
    classDef visual fill:#fce4ec
    classDef data fill:#f1f8e9
    classDef output fill:#e0f2f1
    classDef config fill:#fafafa
    
    class A,B,C entryPoint
    class D,E,F,G,H,I coreAgent
    class L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,AA,BB,CC,DD dependency
    class AB,AC,AD,AE test
    class AF,AG visual
    class AH,AI data
    class AJ,AK,AL output
    class AM,AN,AO,AP config
```

## Data Flow Dependencies

```mermaid
flowchart LR
    %% Input Layer
    A1[Excel File] --> B1[excel_parser_agent.py]
    A2[OpenAI API Key] --> B1
    
    %% Processing Layer
    B1 --> C1[ConstructionItem Objects]
    C1 --> D1[supplier_mapping_agent.py]
    D1 --> E1[Supplier Matches]
    E1 --> F1[communication_agent.py]
    F1 --> G1[Communication Requests]
    G1 --> H1[response_parser_agent.py]
    H1 --> I1[Parsed Responses]
    I1 --> J1[quote_calculator_agent.py]
    J1 --> K1[Calculated Quotes]
    K1 --> L1[document_generator_agent.py]
    
    %% Output Layer
    L1 --> M1[Excel Quotes]
    L1 --> N1[PDF Documents]
    L1 --> O1[Supplier Comparisons]
    
    %% Orchestration
    P1[workflow_orchestrator.py] --> B1
    P1 --> D1
    P1 --> F1
    P1 --> H1
    P1 --> J1
    P1 --> L1
    
    %% Styling
    classDef input fill:#e3f2fd
    classDef processing fill:#f3e5f5
    classDef output fill:#e8f5e8
    classDef orchestration fill:#fff3e0
    
    class A1,A2 input
    class B1,C1,D1,E1,F1,G1,H1,I1,J1,K1,L1 processing
    class M1,N1,O1 output
    class P1 orchestration
```

## Build Order Dependencies

```mermaid
graph TD
    %% Phase 1: Foundation
    A1[system_builder.py] --> B1[excel_parser_agent.py]
    A1 --> C1[requirements.txt]
    
    %% Phase 2: Core Agents
    B1 --> D1[supplier_mapping_agent.py]
    D1 --> E1[communication_agent.py]
    E1 --> F1[response_parser_agent.py]
    F1 --> G1[quote_calculator_agent.py]
    G1 --> H1[document_generator_agent.py]
    
    %% Phase 3: Integration
    H1 --> I1[workflow_orchestrator.py]
    I1 --> J1[test_suite.py]
    
    %% Phase 4: Testing
    J1 --> K1[test_runner.py]
    K1 --> L1[tests/input/]
    K1 --> M1[tests/output/]
    
    %% Phase 5: Visualization
    I1 --> N1[simple_visual_demo.py]
    I1 --> O1[visual_workflow_monitor.py]
    
    %% Phase 6: Documentation
    I1 --> P1[demo_system.py]
    P1 --> Q1[README.md]
    
    %% Styling
    classDef phase1 fill:#e8f5e8
    classDef phase2 fill:#e3f2fd
    classDef phase3 fill:#f3e5f5
    classDef phase4 fill:#fff3e0
    classDef phase5 fill:#fce4ec
    classDef phase6 fill:#fafafa
    
    class A1,B1,C1 phase1
    class D1,E1,F1,G1,H1 phase2
    class I1 phase3
    class J1,K1,L1,M1 phase4
    class N1,O1 phase5
    class P1,Q1 phase6
```

## External Dependencies

```mermaid
graph TD
    %% Python Core
    A[Python 3.8+] --> B[pandas>=1.5.3]
    A --> C[openpyxl>=3.1.2]
    A --> D[openai>=1.0.0]
    A --> E[requests>=2.28.2]
    
    %% Development Tools
    A --> F[pytest>=7.0.0]
    A --> G[black>=23.0.0]
    
    %% System Dependencies
    A --> H[pathlib]
    A --> I[dataclasses]
    A --> J[json]
    A --> K[logging]
    A --> L[re]
    A --> M[time]
    A --> N[subprocess]
    A --> O[concurrent.futures]
    
    %% External Services
    D --> P[OpenAI API]
    E --> Q[HTTP Services]
    
    %% File System
    C --> R[Excel Files]
    B --> S[CSV Files]
    H --> T[File System]
    
    %% Styling
    classDef python fill:#3776ab
    classDef package fill:#ffd43b
    classDef external fill:#ff6b6b
    classDef system fill:#6c757d
    
    class A python
    class B,C,D,E,F,G package
    class H,I,J,K,L,M,N,O system
    class P,Q external
    class R,S,T system
```

## Agent Communication Dependencies

```mermaid
sequenceDiagram
    participant WO as Workflow Orchestrator
    participant EPA as Excel Parser Agent
    participant SMA as Supplier Mapping Agent
    participant CA as Communication Agent
    participant RPA as Response Parser Agent
    participant QCA as Quote Calculator Agent
    participant DGA as Document Generator Agent
    
    WO->>EPA: Parse Excel file
    EPA-->>WO: ConstructionItem list
    
    WO->>SMA: Map suppliers for items
    SMA-->>WO: Supplier mappings
    
    WO->>CA: Send requests to suppliers
    CA-->>WO: Communication results
    
    WO->>RPA: Parse supplier responses
    RPA-->>WO: Parsed quotes
    
    WO->>QCA: Calculate optimal quotes
    QCA-->>WO: Final quotes with pricing
    
    WO->>DGA: Generate documents
    DGA-->>WO: Professional quotes (Excel/PDF)
    
    Note over WO: Complete workflow executed
```

## Error Handling Dependencies

```mermaid
graph TD
    %% Error Sources
    A[File Not Found] --> B[Graceful Degradation]
    C[API Failure] --> B
    D[Invalid Data] --> B
    E[Network Timeout] --> B
    
    %% Error Handling Components
    B --> F[Logging System]
    B --> G[Fallback Mechanisms]
    B --> H[Validation Layers]
    
    %% Recovery Actions
    F --> I[Error Reports]
    G --> J[Alternative Processing]
    H --> K[Data Sanitization]
    
    %% Monitoring
    I --> L[Error Tracking]
    J --> M[Performance Metrics]
    K --> N[Quality Assurance]
    
    %% Styling
    classDef error fill:#ffebee
    classDef handling fill:#e8f5e8
    classDef recovery fill:#e3f2fd
    classDef monitoring fill:#fff3e0
    
    class A,C,D,E error
    class B,F,G,H handling
    class I,J,K recovery
    class L,M,N monitoring
```

## Performance Dependencies

```mermaid
graph LR
    %% Input Size
    A[Small Project<br/>6 items] --> B[15 seconds<br/>$0.02]
    C[Medium Project<br/>11 items] --> D[30 seconds<br/>$0.05]
    E[Large Project<br/>50+ items] --> F[2 minutes<br/>$0.25]
    
    %% Processing Factors
    B --> G[Parallel Processing]
    D --> G
    F --> G
    
    G --> H[OpenAI API Calls]
    G --> I[File I/O Operations]
    G --> J[Memory Usage]
    
    %% Optimization
    H --> K[Batch Processing]
    I --> L[Caching]
    J --> M[Memory Management]
    
    %% Styling
    classDef size fill:#e8f5e8
    classDef performance fill:#e3f2fd
    classDef factors fill:#f3e5f5
    classDef optimization fill:#fff3e0
    
    class A,C,E size
    class B,D,F performance
    class G,H,I,J factors
    class K,L,M optimization
``` 