# 🏗️ Construction Industry Agents - Architecture

## 📊 Domain-Driven Design Structure

```
src/
├── core/                    # Core domain models and interfaces
│   ├── models/             # Domain entities
│   ├── interfaces/         # Abstract interfaces
│   └── exceptions/         # Domain exceptions
│
├── domains/                # Business domains
│   ├── parsing/            # Excel parsing domain
│   ├── suppliers/          # Supplier management domain  
│   ├── communication/      # Communication domain
│   ├── responses/          # Response processing domain
│   ├── quotes/             # Quote calculation domain
│   └── documents/          # Document generation domain
│
├── workflow/               # Workflow orchestration
│   ├── orchestrators/      # Workflow coordinators
│   └── builders/           # System builders
│
├── infrastructure/         # Infrastructure concerns
│   ├── config/            # Configuration
│   ├── persistence/       # Data storage
│   └── external/          # External services
│
├── web/                   # Web interface
│   ├── api/               # REST API
│   └── frontend/          # Web frontend
│
└── testing/               # Testing framework
    ├── framework/         # Test runners
    └── fixtures/          # Test data
```

## 🎯 Domain Responsibilities

### **Parsing Domain**
- Excel file analysis
- Construction item extraction
- Data validation

### **Suppliers Domain** 
- Supplier database management
- Category-based matching
- Performance tracking

### **Communication Domain**
- Multi-channel messaging
- Request templating
- Response tracking

### **Responses Domain**
- Email/PDF parsing
- Price extraction
- Data validation

### **Quotes Domain**
- Price optimization
- Margin calculation
- Business rules

### **Documents Domain**
- Template management
- PDF/Excel generation
- Professional formatting

## 🔄 Data Flow

1. **Parsing** → Extracts construction items
2. **Suppliers** → Maps items to suppliers  
3. **Communication** → Sends requests
4. **Responses** → Processes replies
5. **Quotes** → Calculates optimal pricing
6. **Documents** → Generates deliverables

## 🧪 Testing Strategy

- **Unit Tests**: Each domain isolated
- **Integration Tests**: Cross-domain workflows
- **E2E Tests**: Complete system validation
- **Performance Tests**: Speed and accuracy metrics
