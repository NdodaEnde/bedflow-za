<prd>

# Technical Product Requirements Document: BedFlow SA - Hospital Bed Management System MVP

## 1. Product Overview

BedFlow SA is a real-time bed management system for South African hospitals that tracks bed status, reduces turnover time, and provides actionable insights through an ontology-first approach. The MVP focuses on ICU bed turnover optimization using semantic modeling to translate between healthcare worker mental models and technical data sources.

## 2. User Stories

### Core Bed Management
```gherkin
Feature: Real-time bed status tracking

Scenario: Ward manager views current bed status
  Given I am logged in as a ward manager
  When I access the bed dashboard
  Then I should see all beds in my ward with color-coded status
  And each bed should show time in current state
  And problem beds should be highlighted at the top

Scenario: Nurse updates bed status
  Given I am a nurse on duty
  When I complete cleaning bed 7
  Then I should be able to mark it as "clean_awaiting_verification"
  And the status should update within 5 seconds
  And the ward manager should receive a notification

Scenario: Automatic status detection from MQTT
  Given the MQTT broker publishes a bed occupancy change
  When the system receives the message
  Then the bed status should update automatically
  And the semantic model should derive the business status
  And the UI should reflect the change within 30 seconds

Scenario: Identifying blocked discharge beds
  Given a patient has been approved for discharge
  When more than 30 minutes pass without bed vacancy
  Then the bed should be marked as "blocked_by_family"
  And the revenue loss calculation should begin
  And an alert should be sent to the ward manager

Scenario: Cleaning verification workflow
  Given a bed has been marked as cleaned
  When a nurse inspects the bed
  Then they should be able to verify or reject the cleaning
  And if rejected, the cleaner should be notified
  And the bed should return to "dirty_waiting_cleaner" status

Scenario: Revenue loss tracking
  Given a bed is in a non-productive state
  When I view the bed details
  Then I should see the cumulative revenue loss
  And the time since the bed became non-productive
  And suggested actions to resolve the blockage

Scenario: Emergency admission request
  Given emergency department needs an ICU bed
  When they check bed availability
  Then they should see truly available beds (clean and verified)
  And beds about to be available (discharge in progress)
  And NOT see beds that appear vacant but are dirty

Scenario: Shift handover report
  Given it is shift change time
  When the outgoing nurse generates a handover report
  Then it should list all problem beds
  And beds requiring immediate attention
  And pending cleaning verifications

Scenario: Offline status update
  Given the network connection is intermittent
  When a nurse updates a bed status offline
  Then the update should be queued locally
  And sync when connection is restored
  And conflicts should be resolved by timestamp

Scenario: Multi-ward visibility for matron
  Given I am logged in as a matron
  When I access the hospital overview
  Then I should see all wards' bed utilization
  And identify bottlenecks across departments
  And drill down into specific ward details

Scenario: Ventilator bed management
  Given a bed is equipped with a ventilator
  When the patient no longer needs ventilation
  Then the nurse should be able to downgrade the bed type
  And the bed becomes available for non-ventilated patients
  And emergency is notified of ventilator availability

Scenario: Bed turnover time analytics
  Given beds have been tracked for 7 days
  When I view the analytics dashboard
  Then I should see average turnover time by ward
  And identify patterns by day of week
  And compare against target KPIs

Scenario: POPIA-compliant audit trail
  Given any user accesses patient-related bed information
  When they perform any action
  Then the system should log the access with purpose
  And maintain an immutable audit trail
  And be exportable for compliance reporting

Scenario: Mobile responsiveness for ward rounds
  Given I am doing ward rounds with a tablet
  When I access BedFlow on the tablet
  Then the interface should be touch-optimized
  And load within 2 seconds
  And work in portrait and landscape modes

Scenario: Escalation for long-blocked beds
  Given a bed has been blocked for more than 2 hours
  When the threshold is exceeded
  Then an escalation should trigger automatically
  And notify the matron via WhatsApp
  And appear in the priority action list

Scenario: Bed maintenance scheduling
  Given a bed requires maintenance
  When maintenance is scheduled
  Then the bed should show as unavailable
  And estimated return time should be visible
  And not count against turnover metrics

Scenario: Historical bed state replay
  Given an incident occurred yesterday
  When investigating what happened
  Then I should be able to replay bed states
  And see the sequence of status changes
  And identify where the process broke down

Scenario: Integration with hospital admission system
  Given a patient is admitted through the admission system
  When they are assigned to a bed
  Then BedFlow should receive the assignment
  And update the bed status to occupied
  And link the patient record

Scenario: Cleaning staff workload view
  Given I am a cleaning supervisor
  When I check the cleaning queue
  Then I should see all beds awaiting cleaning
  And approximate time since request
  And be able to assign cleaners to specific beds

Scenario: Real-time occupancy percentage
  Given the CFO needs occupancy metrics
  When they access the executive dashboard
  Then they should see real-time occupancy percentage
  And trending over the past month
  And projected revenue impact
```

## 3. User Flows

### Primary Flow: Bed Turnover Process
1. Patient discharge approved in HIS → HL7 message received
2. System marks bed as "discharge_pending"
3. Patient physically leaves → Nurse updates status via mobile
4. Bed status changes to "dirty_waiting_cleaner"
5. System notifies cleaning staff via dashboard
6. Cleaner begins cleaning → Updates status to "cleaning_in_progress"
7. Cleaner completes → Marks as "cleaned_awaiting_verification"
8. Nurse inspects bed → Verifies or rejects cleaning
9. If verified → Bed becomes "ready_for_admission"
10. System notifies admissions of availability
11. New patient assigned → Bed becomes "occupied"

### Secondary Flow: Problem Bed Escalation
1. Bed remains in problematic state > 30 minutes
2. System calculates revenue loss
3. Alert generated to ward manager dashboard
4. Ward manager reviews blocking reason
5. Manager takes action or escalates to matron
6. Action logged in system
7. If resolved, bed returns to normal flow
8. If not resolved in 2 hours, CFO notified

### Authentication Flow
1. User accesses bedflow.co.za
2. Redirected to login if not authenticated
3. Enters credentials (email/password or hospital ID)
4. System validates against Directus users
5. Loads role-based dashboard
6. Session maintained for 12 hours
7. Auto-refresh token before expiry

## 4. Screens and UI/UX

### Dashboard Screen (Main)
- **Grid View**: Visual bed layout matching physical ward
- **Bed Cards**: Color-coded (green=ready, red=dirty, amber=cleaning, black=blocked)
- **Quick Stats Bar**: Total beds, occupied, available, problems
- **Action Buttons**: Mark cleaned, verify, escalate
- **Filter Controls**: By ward, floor, status, urgency
- **Real-time Updates**: WebSocket connection for live changes

### Bed Detail Modal
- **Current Status**: Large, color-coded status indicator
- **Timeline**: Last 24 hours of state changes
- **Patient Info**: Name (if occupied), expected discharge
- **Actions Available**: Based on current state and user role
- **Revenue Meter**: Real-time loss counter if problematic
- **History Log**: Recent actions taken

### Analytics Dashboard
- **KPI Cards**: Avg turnover time, occupancy rate, revenue impact
- **Time Series Chart**: Turnover trends over time
- **Heat Map**: Problem beds by time of day
- **Comparison Table**: Ward vs ward performance
- **Export Controls**: PDF/CSV download options

### Mobile Ward Round View
- **Simplified Layout**: Single column, large touch targets
- **Swipe Navigation**: Between beds
- **Quick Actions**: Single-tap status updates
- **Offline Indicator**: Connection status badge
- **Voice Notes**: Record observations

### Admin Configuration
- **Bed Management**: Add/remove/configure beds
- **Ward Settings**: Define layouts and relationships
- **User Management**: Roles and permissions
- **Semantic Model Editor**: Define business rules
- **Integration Settings**: MQTT, HL7, DHIS2 endpoints

## 5. Features and Functionality

### Core Features

**Real-time Bed Tracking**
- MQTT subscription to bed sensor topics
- Status derivation through semantic model
- 30-second maximum latency requirement
- Automatic conflict resolution

**Semantic Status Management**
- Business status derived from multiple data sources
- Configurable state machine rules
- Custom status definitions per hospital
- Intelligent state inference

**Revenue Impact Calculation**
- Real-time revenue loss tracking
- Configurable bed rates (ICU: R1200/hour)
- Aggregated reporting by ward/hospital
- Predictive revenue recovery estimates

**Multi-channel Notifications**
- In-app notifications via WebSocket
- WhatsApp integration for critical alerts
- Email digests for management
- Configurable escalation chains

**Offline-First Mobile Support**
- Progressive Web App (PWA)
- Local state management
- Queue-based sync when online
- Conflict resolution by timestamp

**Audit Trail & Compliance**
- Every action logged with user, timestamp, purpose
- POPIA-compliant data handling
- Immutable audit log
- Exportable compliance reports

## 6. Technical Architecture

### High-Level Architecture
```
[MQTT Broker] ──┐
[HL7 Feed] ─────┼──→ [Airbyte] ──→ [DuckDB] ──→ [dbt] ──→ [PostgreSQL]
[DHIS2 API] ────┘                                            │
                                                             ↓
[Mobile PWA] ←──→ [Retool] ←──→ [Directus API] ←──────────→ [Semantic Layer]
                                       ↑
                                 [WebSocket Server]
```

### Technology Stack
- **Data Ingestion**: Airbyte OSS
- **Stream Processing**: DuckDB
- **Transformation**: dbt (data build tool)
- **Database**: PostgreSQL with TimescaleDB
- **API Layer**: Directus (Headless CMS)
- **Frontend**: Retool (Internal Tools)
- **Real-time**: WebSocket (Socket.io)
- **Deployment**: Docker Compose on Hetzner
- **CDN/Proxy**: Cloudflare

## 7. System Design

### Component Breakdown

**Data Ingestion Service**
- Airbyte connectors for MQTT, HL7, DHIS2
- 5-minute sync intervals for batch sources
- Real-time for MQTT streams
- Error handling with exponential backoff

**Semantic Processing Engine**
- dbt models for business logic
- Materialized views for performance
- Incremental updates every 30 seconds
- State machine implementation

**API Gateway (Directus)**
- GraphQL and REST endpoints
- Role-based access control
- Real-time subscriptions
- Webhook triggers for events

**Frontend Application (Retool)**
- Component-based architecture
- Responsive grid system
- WebSocket client for updates
- Local storage for offline queue

**Notification Service**
- WhatsApp Business API integration
- Priority queue for alerts
- Template-based messaging
- Delivery confirmation tracking

## 8. API Specifications

### REST Endpoints

```typescript
// Bed Operations
GET /api/beds
Response: BedEntity[]

GET /api/beds/:id
Response: BedEntity

PATCH /api/beds/:id/status
Body: { status: string, reason?: string }
Response: BedEntity

POST /api/beds/:id/verify-cleaning
Body: { verified: boolean, notes?: string }
Response: CleaningVerification

// Analytics
GET /api/analytics/turnover
Query: ?ward=ICU&period=7d
Response: TurnoverMetrics

GET /api/analytics/revenue-loss
Query: ?date_from=2024-01-01
Response: RevenueLossReport

// Notifications
POST /api/notifications/escalate
Body: { bed_id: string, reason: string, urgency: 'low'|'medium'|'high' }
Response: EscalationTicket
```

### GraphQL Schema

```graphql
type Bed {
  id: ID!
  number: String!
  ward: Ward!
  status: BedStatus!
  semantic_status: String!
  patient: Patient
  time_in_status: Int!
  revenue_loss: Float
  history: [StatusChange!]!
}

type Query {
  beds(ward: ID, status: String): [Bed!]!
  problemBeds(threshold: Int): [Bed!]!
  bedTurnoverMetrics(period: String!): TurnoverMetrics!
}

type Mutation {
  updateBedStatus(id: ID!, status: String!, reason: String): Bed!
  verifyCleaning(bedId: ID!, approved: Boolean!): Bed!
  escalateBed(bedId: ID!, reason: String!): Escalation!
}

type Subscription {
  bedStatusChanged(ward: ID): Bed!
}
```

## 9. Data Model

### Core Entities

```sql
-- Beds (Master)
CREATE TABLE beds (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  bed_number VARCHAR(20) UNIQUE NOT NULL,
  ward_id UUID REFERENCES wards(id),
  bed_type ENUM('standard', 'icu', 'ventilator'),
  semantic_status VARCHAR(50), -- Derived from semantic model
  current_patient_id UUID REFERENCES patients(id),
  last_status_change TIMESTAMP,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Status History (Immutable)
CREATE TABLE bed_status_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  bed_id UUID REFERENCES beds(id),
  status VARCHAR(50) NOT NULL,
  derived_status VARCHAR(50), -- From semantic model
  source VARCHAR(50), -- 'mqtt', 'manual', 'hl7'
  user_id UUID REFERENCES users(id),
  reason TEXT,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Cleaning Verifications
CREATE TABLE cleaning_verifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  bed_id UUID REFERENCES beds(id),
  cleaner_id UUID REFERENCES users(id),
  verifier_id UUID REFERENCES users(id),
  cleaning_started TIMESTAMP,
  cleaning_completed TIMESTAMP,
  verified_at TIMESTAMP,
  approved BOOLEAN,
  rejection_reason TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Revenue Tracking
CREATE TABLE revenue_impacts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  bed_id UUID REFERENCES beds(id),
  blocking_state VARCHAR(50),
  duration_minutes INTEGER,
  hourly_rate DECIMAL(10,2),
  revenue_lost DECIMAL(10,2),
  period_start TIMESTAMP,
  period_end TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Audit Log (POPIA Compliance)
CREATE TABLE audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  action VARCHAR(50) NOT NULL,
  resource_type VARCHAR(50),
  resource_id UUID,
  purpose VARCHAR(100),
  ip_address INET,
  user_agent TEXT,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for Performance
CREATE INDEX idx_beds_ward_status ON beds(ward_id, semantic_status);
CREATE INDEX idx_bed_history_bed_time ON bed_status_history(bed_id, created_at DESC);
CREATE INDEX idx_audit_user_time ON audit_log(user_id, created_at DESC);
CREATE INDEX idx_revenue_bed_period ON revenue_impacts(bed_id, period_start);
```

### Relationships
- One-to-Many: Ward → Beds
- One-to-Many: Bed → Status History
- One-to-One: Bed → Current Patient
- Many-to-Many: Users → Beds (via interactions)

## 10. Security Considerations

### Authentication & Authorization
- JWT-based authentication with 12-hour expiry
- Role-based access control (Nurse, Manager, Admin, Cleaner)
- Multi-factor authentication for admin accounts
- Session management with secure HTTP-only cookies

### Data Protection
- AES-256 encryption for data at rest
- TLS 1.3 for all data in transit
- Patient data hashing for POPIA compliance
- No PII in logs or analytics

### API Security
- Rate limiting: 100 requests/minute per user
- API key authentication for external integrations
- CORS configuration for trusted origins only
- Input validation and sanitization

### Infrastructure Security
- Ubuntu firewall (UFW) with minimal open ports
- SSH key-only authentication
- Regular security updates via unattended-upgrades
- Fail2ban for brute force protection

## 11. Performance Requirements

### Response Times
- Dashboard load: < 2 seconds
- Status update propagation: < 5 seconds
- API response time: < 200ms (p95)
- Mobile app load: < 3 seconds on 3G

### Throughput
- Handle 1000 bed updates/minute
- Support 100 concurrent users
- Process 10,000 MQTT messages/hour
- Generate reports for 500 beds in < 10 seconds

### Availability
- 99.5% uptime SLA
- Maximum planned downtime: 4 hours/month
- Recovery Time Objective (RTO): 1 hour
- Recovery Point Objective (RPO): 5 minutes

## 12. Scalability Considerations

### Horizontal Scaling
- Stateless API design for easy replication
- Load balancer ready (nginx)
- Database read replicas for analytics
- Microservices architecture preparation

### Vertical Scaling
- Initial: 4 vCPU, 8GB RAM (supports 50 beds)
- Growth: 8 vCPU, 16GB RAM (supports 200 beds)
- Migration path to managed services (RDS, etc.)

### Data Partitioning
- Time-series partitioning for historical data
- Archive strategy for data > 1 year
- Separate OLTP and OLAP workflows

## 13. Testing Strategy

### Unit Testing
- dbt model tests for data transformations
- Jest for API endpoint testing
- 80% code coverage target
- Automated on each commit

### Integration Testing
- End-to-end bed status flow
- MQTT → Database → API → UI
- Notification delivery verification
- Offline/online synchronization

### Performance Testing
- JMeter for load testing
- 100 concurrent user simulation
- Stress test at 2x expected load
- Database query performance monitoring

### User Acceptance Testing
- 5-day pilot with single ward
- Shadow operations for 48 hours
- Feedback collection via forms
- Iteration based on nurse feedback

## 14. Deployment Plan

### Phase 1: Infrastructure Setup (Day 1)
```bash
# Hetzner server provisioning
- Ubuntu 22.04 LTS
- Docker & Docker Compose installation
- Cloudflare DNS configuration
- SSL certificate setup

# Initial deployment
docker-compose up -d
```

### Phase 2: Data Pipeline (Day 2-3)
- Configure Airbyte connections
- Deploy dbt models
- Verify MQTT connectivity
- Test data flow end-to-end

### Phase 3: Application Deployment (Day 4)
- Deploy Directus with schema
- Configure Retool dashboards
- Set up WebSocket server
- Configure notification services

### Phase 4: Go-Live (Day 5)
- Final security audit
- User account creation
- Training session recording
- Switch to production mode

### Rollback Plan
- Database backup before deployment
- Previous version in Docker registry
- One-command rollback: `docker-compose down && docker-compose -f docker-compose.backup.yml up`

## 15. Maintenance and Support

### Monitoring
- Uptime monitoring via Uptime Kuma
- Error tracking with Sentry
- Performance monitoring with Grafana
- Daily automated health checks

### Backup Strategy
- Database: Daily automated backups to S3
- Configuration: Git repository
- Recovery testing: Monthly
- 30-day retention policy

### Support Structure
- WhatsApp group for immediate issues
- GitHub Issues for bug tracking
- Weekly review meetings with ward manager
- On-call rotation for critical issues

### Update Cycle
- Security patches: Immediate
- Bug fixes: Weekly release
- Feature updates: Bi-weekly sprint
- Major upgrades: Quarterly with notice

### Documentation
- API documentation via Swagger
- User guides in /docs folder
- Video tutorials for common tasks
- Change log maintained in CHANGELOG.md

</prd>