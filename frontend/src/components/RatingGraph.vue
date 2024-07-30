<template>
    <Bar
      id="my-chart-id"
      :options="chartOptions"
      :data="chartData"
    />
  </template>
  
  <script>
  import { Bar } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
  import axios from 'axios'
  
  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
  
  export default {
    name: 'BarChart',
    components: { Bar },
    data() {
      return {
        chartData: {
            labels: [],
            datasets: []
        },
        chartOptions: {
          responsive: true
        }
      }
    },

  methods: {
    getRandomColor() {
      const letters = '0123456789ABCDEF';
      let color = '#';
      for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    }
  },

    beforeCreate() {
    axios.get('/graphs/books/rating')
      .then(response => {
        const data = response.data;
        const backgroundColors = data.map(() => this.getRandomColor());
        this.chartData = {
          labels: data.map(d => d.name),
          datasets: [{
            data: data.map(d => d.rating),
            backgroundColor: backgroundColors,
            borderColor: backgroundColors,
            borderWidth: 1,
            label: 'Books by rating'

          }]
        };
      })
      .catch(error => {
        console.error('Error fetching chart data:', error);
      });
  }
  }
  </script>