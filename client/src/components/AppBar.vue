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
  import {useI18n} from 'vue-i18n' 


  const {t} = useI18n();


  console.log(t("common.arr[0]"))

  let date = ref("")

  setInterval(updateDate, 1000);
  updateDate();

  function updateDate(): void {
      const now = new Date();
      const dayVal = now.getDay()-1;
      const monthVal = now.getMonth();
      date.value = t("common.weekDays["+dayVal+"]") + ', ' + zeroPadding(now.getDate(), 2) + ' ' + t("common.months["+monthVal+"]") + ' ' + zeroPadding(now.getFullYear(), 4);
  };

  function zeroPadding(num: number, digit: number): string {
      var zero = '';
      for(var i = 0; i < digit; i++) {
          zero += '0';
      }
      return (zero + num).slice(-digit);
  }

</script>