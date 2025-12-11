CREATE TABLE MEMBERSHIP_PLAN (
                                 Plan_ID         INT              PRIMARY KEY,
                                 Plan_Name       VARCHAR(50)     NOT NULL,
                                 Monthly_Fee     DECIMAL(10, 2)  NOT NULL,
                                 Description     TEXT
);

CREATE TABLE MEMBER (
                        Member_ID               INT             PRIMARY KEY,
                        First_Name              VARCHAR(50)     NOT NULL,
                        Last_Name               VARCHAR(50)     NOT NULL,
                        Email                   VARCHAR(100)    NOT NULL,
                        Phone_Number            VARCHAR(20),
                        Membership_Start_Date   DATE            NOT NULL,
                        Plan_ID                 INT             NOT NULL,

                        CONSTRAINT fk_member_plan
                            FOREIGN KEY (Plan_ID)
                                REFERENCES MEMBERSHIP_PLAN(Plan_ID)
);

CREATE TABLE INSTRUCTOR (
                            Instructor_ID   INT              PRIMARY KEY,
                            First_Name      VARCHAR(50)     NOT NULL,
                            Last_Name       VARCHAR(50)     NOT NULL,
                            Specialty       VARCHAR(100)    NOT NULL,
                            Email           VARCHAR(100)    NOT NULL
);

CREATE TABLE FITNESS_CLASS (
                               Class_ID        INT             PRIMARY KEY,
                               Class_Name      VARCHAR(100)    NOT NULL,
                               Scheduled_Date  DATE            NOT NULL,
                               Start_Time      TIME            NOT NULL,
                               End_Time        TIME            NOT NULL,
                               Instructor_ID   INT             NOT NULL,

                               CONSTRAINT fk_class_instructor
                                   FOREIGN KEY (Instructor_ID)
                                       REFERENCES INSTRUCTOR(Instructor_ID)
);


CREATE TABLE CLASS_REGISTRATIONS(
                                    Registration_ID     INT         PRIMARY KEY,
                                    Member_ID           INT         NOT NULL,
                                    Class_ID            INT         NOT NULL,
                                    Registration_Date   DATE        NOT NULL,

                                    CONSTRAINT fk_registration_member
                                        FOREIGN KEY (Member_ID)
                                            REFERENCES MEMBER(Member_ID),

                                    CONSTRAINT fk_registration_class
                                        FOREIGN KEY (Class_ID)
                                            REFERENCES FITNESS_CLASS(Class_ID)


);


