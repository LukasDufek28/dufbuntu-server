<template>
  <div class="calendar-container">
    <h2>Nutrition Calendar</h2>
    <table>
      <thead>
        <tr>
          <th>Date</th>
          <th>Calories</th>
          <th>Protein</th>
          <th>Carbs</th>
          <th>Fat</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="day in calendar" :key="day.date">
          <td>{{ day.date }}</td>
          <td class="calories">{{ day.calories.toFixed(1) }}</td>
          <td class="protein">{{ day.protein.toFixed(1) }}</td>
          <td class="carbs">{{ day.carbs.toFixed(1) }}</td>
          <td class="fat">{{ day.fat.toFixed(1) }}</td>
        </tr>
      </tbody>
    </table>
    <router-link to="/">Back to Add Meal</router-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const calendar = ref([])
const fetchCalendar = async () => {
  const res = await fetch('http://localhost:5000/api/calendar')
  calendar.value = await res.json()
}
onMounted(fetchCalendar)
</script>

<style scoped>
:root {
  --primary: #27ae60;
  --primary-dark: #219150;
  --secondary: #222;
  --card-bg: #181818;
  --border: #333;
  --text: #e8ffe8;
  --shadow: 0 2px 16px 0 #000a;
  --accent-pink: #ff7fd8;
  --accent-blue: #38f9d7;
  --accent-yellow: #ffe066;
  --accent-orange: #ffb347;
}

body {
  background: linear-gradient(120deg, #181818 0%, #232526 100%);
  min-height: 100vh;
}

.calendar-container {
  width: 100vw;
  min-height: 100vh;
  margin: 0;
  background: var(--card-bg);
  border-radius: 0;
  box-shadow: none;
  padding: 3rem 3vw 2rem 3vw;
  color: var(--text);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}

h2 {
  font-weight: 700;
  font-size: 2.3rem;
  margin-bottom: 2rem;
  color: var(--accent-pink);
  text-align: center;
  letter-spacing: 2px;
  text-shadow: 0 2px 8px #38f9d7cc;
}

table {
  width: 100%;
  max-width: 1500px;
  border-collapse: separate;
  border-spacing: 0;
  margin-bottom: 2.5rem;
  background: linear-gradient(90deg, #232526 0%, #27ae60 100%);
  border-radius: 22px;
  overflow: hidden;
  color: var(--text);
  box-shadow: 0 4px 24px 0 #27ae6040, 0 1.5px 8px #ff7fd822;
  font-size: 1.25rem;
}

th, td {
  padding: 1.3rem 1.2rem;
  text-align: center;
}

th {
  background: linear-gradient(90deg, #27ae60 0%, #38f9d7 100%);
  color: #fff;
  font-weight: 700;
  border-bottom: 3px solid var(--accent-pink);
  font-size: 1.15rem;
  letter-spacing: 1px;
}

tr:nth-child(even) td {
  background: #232526cc;
}

tr:nth-child(odd) td {
  background: #181818cc;
}

tr:hover td {
  background: #ff7fd822;
  color: var(--accent-pink);
  transition: background 0.2s, color 0.2s;
}

td.calories { color: var(--accent-yellow); font-weight: 700; }
td.protein { color: var(--accent-blue); font-weight: 700; }
td.carbs { color: var(--accent-orange); font-weight: 700; }
td.fat { color: var(--accent-pink); font-weight: 700; }

a {
  display: block;
  text-align: center;
  margin-top: 1.5rem;
  color: var(--accent-blue);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
  font-size: 1.15rem;
}

a:hover {
  color: var(--accent-pink);
}

/* Mobile styles */
@media (max-width: 800px) {
  .calendar-container {
    padding: 1rem 0.5rem;
  }
  h2 {
    font-size: 1.3rem;
    margin-bottom: 1rem;
  }
  table {
    font-size: 1rem;
    max-width: 100vw;
    min-width: 0;
    border-radius: 12px;
    margin-bottom: 1.2rem;
    overflow-x: auto;
    display: block;
  }
  th, td {
    padding: 0.7rem 0.4rem;
    font-size: 1rem;
    min-width: 80px;
  }
  tr, thead, tbody {
    display: table-row;
    width: 100%;
  }
  a {
    font-size: 1rem;
    margin-top: 1rem;
  }
}
</style>