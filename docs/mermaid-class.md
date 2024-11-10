## Delve

```mermaid
classDiagram
    class SCA
    class Scanner {
        +string name
        +int id
        +Callable scan_type
    }
    SCA --> Scanner
    Scanner --> Tool1
    Scanner --> Tool2
    Tool1 --> Brimstone
    Tool1 --> ForceBuild
    Tool2 --> StrategyPhaser
    Tool2 --> StratergyInertia
```
