<script setup>
import { ref, onMounted, computed } from 'vue'
const foods = ref([])
const selectedFood = ref(null)
const quantity = ref(100)
const summary = ref(null)
const today = new Date().toISOString().slice(0, 10)

// User info
const height = ref('')
const weight = ref('')
const gender = ref('male')

// Ideal weight calculation (Devine formula)
const idealWeight = computed(() => {
  if (!height.value) return ''
  const h = Number(height.value)
  if (gender.value === 'male') {
    return (50 + 0.91 * (h - 152.4)).toFixed(1)
  } else {
    return (45.5 + 0.91 * (h - 152.4)).toFixed(1)
  }
})

// Daily calorie needs (Mifflin-St Jeor, sedentary)
const dailyCalories = computed(() => {
  if (!height.value || !weight.value) return ''
  const h = Number(height.value)
  const w = Number(weight.value)
  // Assume age 30, activity factor 1.4
  if (gender.value === 'male') {
    const bmr = 10 * w + 6.25 * h - 5 * 30 + 5
    return Math.round(bmr * 1.4)
  } else {
    const bmr = 10 * w + 6.25 * h - 5 * 30 - 161
    return Math.round(bmr * 1.4)
  }
})

// Calories for ideal weight
const idealCalories = computed(() => {
  if (!height.value) return ''
  const h = Number(height.value)
  const iw = gender.value === 'male'
    ? 50 + 0.91 * (h - 152.4)
    : 45.5 + 0.91 * (h - 152.4)
  // Assume age 30, activity factor 1.4
  if (gender.value === 'male') {
    const bmr = 10 * iw + 6.25 * h - 5 * 30 + 5
    return Math.round(bmr * 1.4)
  } else {
    const bmr = 10 * iw + 6.25 * h - 5 * 30 - 161
    return Math.round(bmr * 1.4)
  }
})

const fetchFoods = async () => {
  const res = await fetch('http://localhost:5000/api/foods')
  foods.value = await res.json()
  if (foods.value.length) selectedFood.value = foods.value[0].id
}
const fetchSummary = async () => {
  const res = await fetch(`http://localhost:5000/api/daily_summary/${today}`)
  summary.value = await res.json()
}
const addMeal = async () => {
  await fetch('http://localhost:5000/api/log_meal', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      date: today,
      food_id: selectedFood.value,
      quantity: quantity.value
    })
  })
  fetchSummary()
}

onMounted(() => {
  fetchFoods()
  fetchSummary()
})
</script>

<template>
  <div class="main-container">
    <h2>Add Meal</h2>
    <div class="flex-row">
      <!-- Meal Logging Section (now on the left) -->
      <div class="meal-form-box">
        <form class="meal-form" @submit.prevent="addMeal">
          <select v-model="selectedFood">
            <option v-for="food in foods" :key="food.id" :value="food.id">
              {{ food.name }} (per 100g: {{ food.calories }} kcal, P:{{ food.protein }}, C:{{ food.carbs }}, F:{{ food.fat }})
            </option>
          </select>
          <input type="number" v-model="quantity" placeholder="Quantity (g)" min="1" required />
          <button type="submit">Add</button>
        </form>
      </div>

      <!-- User Info Section (now on the right) -->
      <div class="user-info-box">
        <form class="user-info" @submit.prevent>
          <div class="user-fields">
            <label>
              Height (cm)
              <input type="number" v-model="height" min="100" max="250" required />
            </label>
            <label>
              Weight (kg)
              <input type="number" v-model="weight" min="30" max="300" required />
            </label>
            <label>
              Gender
              <select v-model="gender">
                <option value="male">Male</option>
                <option value="female">Female</option>
              </select>
            </label>
          </div>
          <div class="user-results" v-if="height && weight">
            <div>
              <strong>Ideal Weight:</strong> {{ idealWeight }} kg
            </div>
            <div>
              <strong>Calories to maintain current weight:</strong> {{ dailyCalories }} kcal/day
            </div>
            <div>
              <strong>Calories for ideal weight:</strong> {{ idealCalories }} kcal/day
            </div>
          </div>
        </form>
      </div>
    </div>
    <h3>Today's Summary</h3>
    <div class="summary-box" v-if="summary">
      <div class="summary-row">
        <span class="summary-label calories">Calories:</span>
        <span class="summary-value calories">{{ summary.calories.toFixed(1) }} kcal</span>
      </div>
      <div class="summary-row">
        <span class="summary-label protein">Protein:</span>
        <span class="summary-value protein">{{ summary.protein.toFixed(1) }} g</span>
      </div>
      <div class="summary-row">
        <span class="summary-label carbs">Carbs:</span>
        <span class="summary-value carbs">{{ summary.carbs.toFixed(1) }} g</span>
      </div>
      <div class="summary-row">
        <span class="summary-label fat">Fat:</span>
        <span class="summary-value fat">{{ summary.fat.toFixed(1) }} g</span>
      </div>
    </div>
    <router-link to="/calendar">Go to Calendar</router-link>
  </div>
</template>

<style scoped>
:root {
  --primary: #27ae60;
  --primary-dark: #219150;
  --secondary: #222;
  --card-bg: #181818;
  --border: #333;
  --text: #e8ffe8;
  --shadow: 0 2px 16px 0 #000a;
  --summary-bg: linear-gradient(90deg, #27ae60 0%, #43e97b 50%, #38f9d7 100%);
  --summary-text: #fff;
  --accent-pink: #ff7fd8;
  --accent-blue: #38f9d7;
  --accent-yellow: #ffe066;
  --accent-orange: #ffb347;
}

html, body, #app {
  height: 100%;
  min-height: 100vh;
  margin: 0;
  padding: 0;
}

body {
  background: linear-gradient(120deg, #181818 0%, #232526 100%);
  min-height: 100vh;
}

.main-container {
  width: 100vw;
  min-height: 100vh;
  margin: 0;
  background: var(--card-bg);
  border-radius: 0;
  box-shadow: none;
  padding: 2.5rem 2vw 1.5rem 2vw;
  color: var(--text);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}

h2 {
  font-weight: 700;
  font-size: 2.2rem;
  margin-bottom: 1.5rem;
  color: var(--accent-pink);
  text-align: center;
  letter-spacing: 2px;
  text-shadow: 0 2px 8px #38f9d7cc;
}

.flex-row {
  display: flex;
  gap: 2.5rem;
  justify-content: center;
  align-items: flex-start;
  flex-wrap: nowrap;
  width: 100%;
  max-width: 1800px;
}

.meal-form-box,
.user-info-box {
  flex: 1 1 500px;
  min-width: 350px;
  background: linear-gradient(135deg, #232526 0%, #27ae60 100%);
  border-radius: 16px;
  box-shadow: 0 2px 16px #27ae6040, 0 1.5px 8px #ff7fd822;
  padding: 1.7rem 1.5rem 1.2rem 1.5rem;
  border: 2.5px solid var(--accent-blue);
  margin-bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  max-width: 700px;
  color: var(--text);
  position: relative;
  overflow: hidden;
}

.meal-form-box::before {
  content: "";
  position: absolute;
  top: -40px; left: -40px;
  width: 120px; height: 120px;
  background: var(--accent-pink);
  opacity: 0.08;
  border-radius: 50%;
  z-index: 0;
}
.user-info-box::after {
  content: "";
  position: absolute;
  bottom: -40px; right: -40px;
  width: 120px; height: 120px;
  background: var(--accent-yellow);
  opacity: 0.10;
  border-radius: 50%;
  z-index: 0;
}

.meal-form, .user-info {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
  z-index: 1;
}

.meal-form select,
.meal-form input[type="number"] {
  padding: 0.8rem 1rem;
  border: 1.5px solid var(--accent-blue);
  border-radius: 10px;
  font-size: 1rem;
  background: #232526;
  color: var(--accent-yellow);
  transition: border 0.2s, box-shadow 0.2s;
}

.meal-form select:focus,
.meal-form input[type="number"]:focus {
  border: 1.5px solid var(--accent-pink);
  outline: none;
}

.meal-form button {
  background: linear-gradient(90deg, var(--primary) 0%, var(--accent-pink) 100%);
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 0.9rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  box-shadow: 0 2px 8px 0 #ff7fd822;
}

.meal-form button:hover {
  background: linear-gradient(90deg, var(--accent-pink) 0%, var(--primary) 100%);
}

.user-fields {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.user-info label {
  display: flex;
  flex-direction: column;
  color: var(--accent-yellow);
  font-size: 1rem;
  font-weight: 500;
}

.user-info input,
.user-info select {
  margin-top: 0.3rem;
  background: #232526;
  color: var(--accent-blue);
  border: 1px solid var(--accent-pink);
  border-radius: 6px;
  padding: 0.5rem 0.7rem;
}

.user-results {
  margin-top: 0.5rem;
  color: var(--accent-pink);
  font-size: 1.08rem;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

h3 {
  font-size: 1.5rem;
  color: var(--primary);
  margin: 2.5rem 0 1rem 0;
  text-align: center;
  font-weight: 700;
  letter-spacing: 1px;
  text-shadow: 0 2px 8px #38f9d7cc;
}

.summary-box {
  width: 100%;
  max-width: 1460px;
  min-height: 70px;
  margin: 0 auto 1.5rem auto;
  background: var(--summary-bg);
  border-radius: 22px;
  box-shadow: 0 4px 24px 0 #27ae6040, 0 1.5px 8px #ff7fd822;
  padding: 1.1rem 2rem 1.1rem 2rem;
  color: var(--summary-text);
  font-size: 1.25rem;
  font-weight: 600;
  text-align: center;
  border: 3px solid var(--accent-blue);
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  gap: 2.5rem;
  transition: background 0.3s;
}
</style>