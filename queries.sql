
SELECT * FROM student_schema.students;

-- Join to get student details with gender and major names
SELECT s.student_id, s.name, s.age, g.gender_name, y.year_name, m.major_name, s.monthly_gas_expenses
FROM student_schema.students s
JOIN student_schema.genders g ON s.gender_id = g.gender_id
JOIN student_schema.years_in_school y ON s.year_id = y.year_id
JOIN student_schema.majors m ON s.major_id = m.major_id;
