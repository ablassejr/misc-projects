
INSERT INTO MEMBERSHIP_PLAN (Plan_Name, Monthly_Fee, Description, Plan_ID) VALUES
                                                                      ('Basic', 29.99, 'Access to gym equipment and locker rooms during standard hours (6 AM - 9 PM)', 1),
                                                                      ('Premium', 59.99, 'Unlimited access to all facilities, group classes included, and 24/7 gym access', 2),
                                                                      ('Student', 19.99, 'Discounted rate for enrolled university students with valid student ID', 0);

INSERT INTO INSTRUCTOR (First_Name, Last_Name, Specialty, Email, INSTRUCTOR_ID) VALUES
                                                                     ('Sarah', 'Johnson', 'Yoga', 'sarah.johnson@university.edu', 0),
                                                                     ('Michael', 'Rodriguez', 'HIIT', 'michael.rodriguez@university.edu', 1),
                                                                     ('Emily', 'Chen', 'Strength Training', 'emily.chen@university.edu', 2);

INSERT INTO MEMBER (First_Name, Last_Name, Email, Phone_Number, Membership_Start_Date, Plan_ID, Member_ID) VALUES
                                                                                                    ('John', 'Smith', 'john.smith@email.com', '555-0101', '2025-01-15', 2, 0),
                                                                                                    ('Jessica', 'Brown', 'jessica.brown@email.com', '555-0102', '2025-02-01', 0, 1),
                                                                                                    ('Robert', 'Davis', 'robert.davis@email.com', '555-0103', '2024-09-10', 1, 2);

INSERT INTO FITNESS_CLASS (Class_Name, Scheduled_Date, Start_Time, End_Time, Instructor_ID, Class_ID) VALUES
                                                                                                ('Morning Yoga Flow', '2025-06-16', '07:00:00', '08:00:00', 0, 0),
                                                                                                ('HIIT 30-Min Blast', '2025-06-16', '12:00:00', '12:30:00', 1, 1),
                                                                                                ('Evening Strength', '2025-06-16', '18:00:00', '19:00:00', 2, 2);

INSERT INTO CLASS_REGISTRATIONS (Member_ID, Class_ID, Registration_Date, Registration_ID) VALUES
                                                                            (0, 0, '2025-06-10',0),
                                                                            (0, 2, '2025-06-11',1),
                                                                            (1, 0, '2025-06-12', 2),
                                                                            (1, 1, '2025-06-12', 3),
                                                                            (2, 2, '2025-06-13', 4),
                                                                            (2, 1, '2025-06-14', 5);
