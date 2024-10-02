<template>
    <v-sheet class="pa-0 ma-3 rounded-lg" :height="cellHeight">
      <v-row no-gutters>
        <v-col class="text-center">
          <p class="mt-n5 mb-3 text-white" style="font-size: 14px; height: 18px; ">Ambiente</p>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col class="text-center mt-4" >
          <p style="font-size: 20px;">Temperatura: {{ temperature }}</p>     
        </v-col>
      </v-row>
      <v-row>
        <v-col class="text-center my-0" >
          <p style="font-size: 20px;">Umidità: {{ humidity }}</p>
        </v-col>
      </v-row>
    </v-sheet>
</template>

<script setup lang="ts">
import { socket } from "@/socket";
import { onMounted, ref } from 'vue';

const props = defineProps({
    cellHeight: { type: Number, required: true }
})

const temperature = ref(0)
const humidity = ref(0)

onMounted(() => {
  console.log("mountAmbientData")
  socket.on("ambientData", (data: {temperature:number, humidity:number}) => {
    console.log("receive ambient data ") 
    temperature.value = data.temperature
    humidity.value = data.humidity
  });
})



</script>