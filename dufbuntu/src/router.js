import { createRouter, createWebHistory } from 'vue-router'
import HomePage from './components/HomePage.vue'
import CalendarPage from './components/CalendarPage.vue'

const routes = [
  { path: '/', component: HomePage },
  { path: '/calendar', component: CalendarPage }
]

export default createRouter({
  history: createWebHistory(),
  routes
})