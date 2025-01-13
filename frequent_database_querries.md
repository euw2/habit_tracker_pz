# Najczęściej wykorzystywane zapytania

### 1. Pobierz wszystkie aktywności dla konkretnego użytkownika
```sql
SELECT * FROM Activity WHERE user_id = ?;
```

### 2. Pobierz wszystkie nawyki dla konkretnego użytkownika
```sql
SELECT Habit.* FROM Habit
JOIN Activity ON Habit.id = Activity.habit_id
WHERE Activity.user_id = ?;
```

### 3. Pobierz statystyki nawyków dla konkretnego użytkownika i nawyku
```sql
SELECT * FROM Habit_Statistics
WHERE user_id = ? AND habit_id = ?;
```

### 4. Pobierz łączną liczbę ukończonych nawyków dla konkretnego użytkownika
```sql
SELECT SUM(total_completed) FROM Habit_Statistics
WHERE user_id = ?;
```

### 5. Pobierz najnowszą aktywność dla konkretnego użytkownika
```sql
SELECT * FROM Activity
WHERE user_id = ?
ORDER BY date DESC
LIMIT 1;
```