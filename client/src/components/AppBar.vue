<template>
    <v-row class="text-center">
      <v-col align-self="center" class="text-left">
        <DigitalClock />
      </v-col>

      <v-spacer></v-spacer>

      <v-col align-self="center" class="text-center">
        {{ date }}
      </v-col>

      <v-spacer></v-spacer>

      <v-col align-self="center" class="text-right pr-6">
        <v-btn variant="outlined" rounded>Find my phone</v-btn>
      </v-col>
    </v-row>

</template>

<script setup lang="ts">

  import { ref } from 'vue';
  import DigitalClock from './DigitalClock.vue';

  let date = ref("")

  let week: Array<string> = ['Domenica', 'Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato'];
  let months: Array<string> = ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre'];
  setInterval(updateDate, 1000);
  updateDate();

  function updateDate(): void {
      var now = new Date();
      date.value = week[now.getDay()] + ', ' + zeroPadding(now.getDate(), 2) + ' ' + months[now.getMonth()] + ' ' + zeroPadding(now.getFullYear(), 4);
  };

  function zeroPadding(num: number, digit: number): string {
      var zero = '';
      for(var i = 0; i < digit; i++) {
          zero += '0';
      }
      return (zero + num).slice(-digit);
  }

</script>