<template>
    <v-sheet class="pa-0 ma-3 rounded-lg" :height="cellHeight">
      <v-row no-gutters>
        <v-col class="text-center">
          <p class="mt-n5 mb-3 text-white" style="font-size: 14px; height: 18px; ">Rifiuti</p>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col class="text-center mt-4" >
          <p style="font-size: 20px;">Oggi: {{ todayTrash }}</p>     
        </v-col>
      </v-row>
      <v-row>
        <v-col class="text-center my-0" >
          <p style="font-size: 20px;">Domani: {{ tomorrowTrash }}</p>
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

const todayTrash = ref("--")
const tomorrowTrash = ref("--")

onMounted(async () => {

  // Once created ask for trash data
  interface serverResponse {today:any, tomorrow:any, result:string}
  const resp: serverResponse = await socket.emitWithAck("getTrash")
  if(resp.result === "OK") {
    if(resp.today === "--")
      resp.today = [resp.today]

    if(resp.tomorrow === "--")
      resp.tomorrow = [resp.tomorrow]

    setTrashData({today:resp.today, tomorrow:resp.tomorrow})
  }

  // Register for trash data events emitted from server
  socket.on("trashData", (data: {today:Array<string>, tomorrow:Array<string>}) => {
    setTrashData(data)
  });
})

function setTrashData(data: {today:Array<string>, tomorrow:Array<string>}) {
  console.log(typeof data.today, data.today)
  console.log(typeof data.tomorrow, data.tomorrow)
  todayTrash.value = data.today.join(", ")
  tomorrowTrash.value = data.tomorrow.join(", ")
}




</script>