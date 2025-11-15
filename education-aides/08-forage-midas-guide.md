# Forage Midas - Education Aide
## Understanding Enterprise Spring Boot, Kafka, and Microservices Architecture

### Overview
This guide will help you understand the JPMC Midas financial transaction management system, covering Spring Boot, Apache Kafka, JPA/Hibernate, and microservices patterns.

---

## Part 1: The Big Picture

### What is Midas?

**Project Context:** JPMC (JPMorgan Chase) Advanced Software Engineering Forage Program

**System Purpose:** Financial transaction management and processing

**Key Components:**
```
User Transaction Request
         ↓
    Kafka Topic
         ↓
  Transaction Listener
         ↓
  Business Logic (Services)
         ↓
   Database (H2/JPA)
         ↓
  User Balance Updated
```

**Question:** Why use Kafka for transaction processing?

<details>
<summary>Event-Driven Architecture</summary>

**Traditional Approach:**
```
Client → REST API → Direct DB Update
```
Problems:
- Tight coupling
- No audit trail
- Difficult to scale
- No retry mechanism

**Event-Driven with Kafka:**
```
Client → Kafka → Listener → Process → DB
```
Benefits:
- Decoupling (services independent)
- Event sourcing (full history)
- Scalability (multiple consumers)
- Fault tolerance (retry, replay)
- Asynchronous processing
</details>

---

## Part 2: Spring Boot Fundamentals

### What is Spring Boot?

**Question:** What problem does Spring Boot solve?

<details>
<summary>Spring Boot Overview</summary>

**Before Spring Boot (Spring Framework):**
```xml
<!-- Hundreds of lines of XML configuration -->
<bean id="dataSource" class="...">
  <property name="url" value="..."/>
  <property name="username" value="..."/>
  <!-- ... many more properties ... -->
</bean>
```

**With Spring Boot:**
```yaml
# application.yml
spring:
  datasource:
    url: jdbc:h2:mem:testdb
    username: sa
```

**Key Features:**
1. **Auto-configuration** - Sensible defaults
2. **Starter dependencies** - Pre-configured packages
3. **Embedded server** - No need for external Tomcat
4. **Production-ready** - Metrics, health checks built-in

**The Magic:**
```java
@SpringBootApplication  // This one annotation does a lot!
public class MidasCoreApplication {
    public static void main(String[] args) {
        SpringApplication.run(MidasCoreApplication.class, args);
    }
}
```

**What @SpringBootApplication does:**
- `@Configuration` - Marks as config class
- `@EnableAutoConfiguration` - Auto-configures beans
- `@ComponentScan` - Scans for components
</details>

### Dependency Injection (DI)

**Core Concept:** Don't create objects yourself; let Spring manage them.

**Example:**
```java
// ❌ Without DI (tight coupling)
public class TransactionService {
    private UserRepository repository = new UserRepository();
    // Now we're stuck with this implementation!
}

// ✓ With DI (loose coupling)
@Service
public class TransactionService {
    private final UserRepository repository;

    @Autowired
    public TransactionService(UserRepository repository) {
        this.repository = repository;
    }
    // Spring injects the repository!
}
```

**Benefits:**
- Easy to test (inject mocks)
- Easy to change implementations
- Single Responsibility Principle

---

## Part 3: Understanding the Domain Model

### Entity: UserRecord

**Study the entity structure:**
```java
@Entity
public class UserRecord {
    @Id
    private String userId;

    private String name;

    @OneToOne(cascade = CascadeType.ALL)
    private Balance balance;

    @OneToMany(cascade = CascadeType.ALL)
    private List<Transaction> transactions;
}
```

**Question:** What do these annotations mean?

<details>
<summary>JPA Annotations Explained</summary>

**@Entity:**
- Marks class as JPA entity
- Maps to database table
- Managed by persistence context

**@Id:**
- Marks primary key field
- Uniquely identifies each record

**@OneToOne:**
- Relationship mapping
- One user has one balance
- `cascade = CascadeType.ALL` means operations cascade (save user → saves balance)

**@OneToMany:**
- Relationship mapping
- One user has many transactions
- Bidirectional relationship possible

**Database Schema:**
```sql
CREATE TABLE USER_RECORD (
    user_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    balance_id BIGINT
);

CREATE TABLE BALANCE (
    id BIGINT PRIMARY KEY,
    amount DECIMAL
);

CREATE TABLE TRANSACTION (
    id BIGINT PRIMARY KEY,
    user_id VARCHAR(255),
    amount DECIMAL,
    timestamp TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES USER_RECORD(user_id)
);
```
</details>

### Value Objects: Balance and Transaction

**Question:** What's the difference between an Entity and a Value Object?

<details>
<summary>Domain-Driven Design Concepts</summary>

**Entity:**
- Has identity (ID)
- Mutable (can change over time)
- Lifecycle matters
- Example: UserRecord

**Value Object:**
- No identity
- Immutable (ideally)
- Defined by attributes
- Example: Balance, Transaction (arguable)

**Example:**
```java
public class Balance {
    private BigDecimal amount;  // Use BigDecimal for money!

    public Balance(BigDecimal amount) {
        this.amount = amount;
    }

    public Balance add(BigDecimal value) {
        return new Balance(amount.add(value));  // Immutable!
    }
}
```

**Why BigDecimal for money?**
```java
// ❌ NEVER use double for money!
double money = 0.1 + 0.2;
System.out.println(money);  // 0.30000000000000004 !!!

// ✓ Always use BigDecimal
BigDecimal money = new BigDecimal("0.1").add(new BigDecimal("0.2"));
System.out.println(money);  // 0.3 ✓
```
</details>

---

## Part 4: Apache Kafka Integration

### What is Kafka?

**Question:** How is Kafka different from a traditional message queue?

<details>
<summary>Kafka Fundamentals</summary>

**Message Queue (RabbitMQ, etc.):**
```
Producer → Queue → Consumer
(Message deleted after consumption)
```

**Kafka:**
```
Producer → Topic (Append-only log) → Consumer(s)
           [msg1][msg2][msg3][msg4]...
           (Messages retained!)
```

**Key Differences:**

| Aspect | Queue | Kafka |
|--------|-------|-------|
| Retention | Delete after read | Configurable (days/forever) |
| Consumers | Competing | Multiple independent |
| Ordering | No guarantee | Guaranteed per partition |
| Speed | Moderate | Very high throughput |

**Kafka Architecture:**
```
Topic: "transactions"
├── Partition 0: [msg1, msg4, msg7, ...]
├── Partition 1: [msg2, msg5, msg8, ...]
└── Partition 2: [msg3, msg6, msg9, ...]

Each partition is ordered
Messages distributed by key (or round-robin)
```
</details>

### Transaction Listener

**Study the Kafka consumer:**
```java
@Component
public class TransactionListener {

    @KafkaListener(topics = "transactions", groupId = "midas-core")
    public void consumeTransaction(Transaction transaction) {
        // Process transaction
        processTransaction(transaction);
    }
}
```

**Question:** What does @KafkaListener do?

<details>
<summary>Spring Kafka Integration</summary>

**@KafkaListener:**
- Subscribes to Kafka topic
- Automatically deserializes messages
- Handles errors and retries
- Manages offsets (tracking what's been processed)

**Configuration (application.yml):**
```yaml
spring:
  kafka:
    bootstrap-servers: localhost:9092
    consumer:
      group-id: midas-core
      auto-offset-reset: earliest
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
      properties:
        spring.json.trusted.packages: "*"
```

**Consumer Groups:**
```
Topic: transactions
Message: transaction-001

Consumer Group "midas-core":
├── Consumer 1 (processes partitions 0, 1)
└── Consumer 2 (processes partition 2)

Only ONE consumer in group processes each message!
```

**Offset Management:**
```
Partition 0: [msg1][msg2][msg3][msg4][msg5]
                            ↑
                         Offset 3
                     (Next: msg4)
```
</details>

---

## Part 5: Repository Pattern (Spring Data JPA)

### UserRepository

**Study the repository:**
```java
@Repository
public interface UserRepository extends JpaRepository<UserRecord, String> {
    Optional<UserRecord> findByUserId(String userId);
    List<UserRecord> findByNameContaining(String name);
}
```

**Question:** Where's the implementation?

<details>
<summary>Spring Data JPA Magic</summary>

**Spring Data JPA generates implementation at runtime!**

**Method Naming Convention:**
```java
findBy + Field + Condition

Examples:
findByUserId(String id)              → WHERE user_id = ?
findByNameContaining(String name)    → WHERE name LIKE %?%
findByBalanceGreaterThan(BigDecimal) → WHERE balance > ?
findByNameAndAge(String, int)        → WHERE name = ? AND age = ?
```

**Generated SQL:**
```sql
-- findByUserId("user123")
SELECT * FROM user_record WHERE user_id = 'user123';

-- findByNameContaining("John")
SELECT * FROM user_record WHERE name LIKE '%John%';
```

**Custom Queries:**
```java
@Query("SELECT u FROM UserRecord u WHERE u.balance.amount > :amount")
List<UserRecord> findRichUsers(@Param("amount") BigDecimal amount);

@Query(value = "SELECT * FROM user_record WHERE name = ?1", nativeQuery = true)
List<UserRecord> findByNameNative(String name);
```

**CRUD Operations (inherited from JpaRepository):**
```java
userRepository.save(user);           // INSERT or UPDATE
userRepository.findById(id);         // SELECT by ID
userRepository.findAll();            // SELECT all
userRepository.delete(user);         // DELETE
userRepository.count();              // COUNT
userRepository.existsById(id);       // EXISTS
```
</details>

---

## Part 6: Service Layer

### TransactionService

**Example service:**
```java
@Service
@Transactional
public class TransactionService {

    private final UserRepository userRepository;

    @Autowired
    public TransactionService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public void processTransaction(Transaction transaction) {
        UserRecord user = userRepository.findByUserId(transaction.getUserId())
            .orElseThrow(() -> new UserNotFoundException(transaction.getUserId()));

        Balance currentBalance = user.getBalance();
        Balance newBalance = currentBalance.add(transaction.getAmount());

        user.setBalance(newBalance);
        user.getTransactions().add(transaction);

        userRepository.save(user);
    }
}
```

**Question:** What does @Transactional do?

<details>
<summary>Transaction Management</summary>

**ACID Properties:**
- **Atomicity**: All or nothing
- **Consistency**: Valid state always
- **Isolation**: Transactions don't interfere
- **Durability**: Committed changes persist

**@Transactional ensures:**
```java
@Transactional
public void processTransaction(Transaction tx) {
    // BEGIN TRANSACTION
    try {
        updateBalance();
        addTransaction();
        sendNotification();
        // COMMIT
    } catch (Exception e) {
        // ROLLBACK
        throw e;
    }
}
```

**Without @Transactional:**
```
1. Update balance ✓
2. Add transaction ✓
3. Send notification ❌ (fails)
Result: Inconsistent state! Balance updated but transaction not recorded
```

**With @Transactional:**
```
1. Update balance ✓
2. Add transaction ✓
3. Send notification ❌ (fails)
→ ROLLBACK
Result: Nothing changed! (Consistent state)
```

**Transaction Propagation:**
```java
@Transactional(propagation = Propagation.REQUIRED)  // Default
@Transactional(propagation = Propagation.REQUIRES_NEW)  // New transaction
@Transactional(readOnly = true)  // Optimization for reads
```
</details>

---

## Part 7: Testing

### Unit Testing with Mockito

**Example test:**
```java
@SpringBootTest
class TransactionServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private TransactionService transactionService;

    @Test
    void processTransaction_ShouldUpdateBalance() {
        // Arrange
        UserRecord user = new UserRecord("user1", "John");
        user.setBalance(new Balance(new BigDecimal("100")));

        when(userRepository.findByUserId("user1"))
            .thenReturn(Optional.of(user));

        Transaction tx = new Transaction("user1", new BigDecimal("50"));

        // Act
        transactionService.processTransaction(tx);

        // Assert
        verify(userRepository).save(any(UserRecord.class));
        assertEquals(new BigDecimal("150"), user.getBalance().getAmount());
    }
}
```

**Testing Kafka:**
```java
@SpringBootTest
@EmbeddedKafka(partitions = 1, topics = {"transactions"})
class TransactionListenerTest {

    @Autowired
    private KafkaTemplate<String, Transaction> kafkaTemplate;

    @Test
    void shouldConsumeTransaction() throws InterruptedException {
        // Send message to Kafka
        Transaction tx = new Transaction("user1", new BigDecimal("100"));
        kafkaTemplate.send("transactions", tx);

        // Wait for processing
        Thread.sleep(1000);

        // Verify processing occurred
        // (Check database, mock verification, etc.)
    }
}
```

---

## Part 8: Hands-On Exercises

### Exercise 1: Add Transaction History Endpoint
**Task:** Create REST API to get user transaction history

**Requirements:**
```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping("/{userId}/transactions")
    public List<Transaction> getTransactions(@PathVariable String userId) {
        // Implement this
    }
}
```

### Exercise 2: Implement Withdrawal
**Task:** Add support for withdrawals (negative amounts)

**Validation:**
- Prevent overdraft (balance < 0)
- Throw InsufficientFundsException

### Exercise 3: Add Transaction Types
**Task:** Support different transaction types (DEPOSIT, WITHDRAWAL, TRANSFER)

**Enum:**
```java
public enum TransactionType {
    DEPOSIT,
    WITHDRAWAL,
    TRANSFER
}
```

### Exercise 4: Implement Idempotency
**Task:** Prevent duplicate transaction processing

**Approach:**
- Add transaction ID
- Check if already processed
- Use Redis or database for deduplication

---

## Part 9: First Principles Summary

### Spring Boot Core Concepts

**1. Dependency Injection:**
- Inversion of Control
- Constructor injection (preferred)
- Loose coupling

**2. Annotations:**
- `@Component`, `@Service`, `@Repository`
- `@Autowired`
- `@Transactional`

**3. Auto-configuration:**
- Sensible defaults
- Override with properties
- Conditional beans

### Kafka Concepts

**1. Topics and Partitions:**
- Logical grouping (topic)
- Physical distribution (partitions)
- Ordering per partition

**2. Consumer Groups:**
- Load balancing
- Fault tolerance
- Offset management

**3. At-Least-Once vs Exactly-Once:**
- Delivery guarantees
- Idempotency importance

### JPA/Hibernate

**1. ORM (Object-Relational Mapping):**
- Objects ↔ Tables
- Relationships
- Lazy/Eager loading

**2. Repositories:**
- Data access abstraction
- Method naming convention
- Custom queries

**3. Transactions:**
- ACID properties
- Isolation levels
- Rollback handling

---

## How to Use This Guide with Claude Code CLI

```bash
claude code

# Ask questions like:
"Explain how Spring dependency injection works"
"Walk me through implementing Exercise 1"
"How does Kafka offset management work?"
"Help me debug a JPA lazy loading issue"
"Explain @Transactional propagation"
"How do I test Kafka listeners?"
"Guide me through adding a new REST endpoint"
```
