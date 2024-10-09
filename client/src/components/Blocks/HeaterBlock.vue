<template>
    <v-sheet class="pa-0 ma-3 rounded-lg" :height="cellHeight">
      <v-row no-gutters>
        <v-col class="text-center">
          <p class="mt-n5 mb-3 text-white" style="font-size: 14px; height: 18px; ">{{ t("heater.heaterLabel") }}</p>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col class="text-center" >
          <v-btn stacked height="60px" width="20px" @click="turnOnHeater(60)" class="px-0">
            <template #prepend>
              <v-icon :icon="mdiPower" :size="30"></v-icon>
            </template>
            <p style="font-size: 10px; height: 25px;">{{ t("heater.turnOn60") }}</p>
          </v-btn>
        </v-col> 
        <v-col class="text-center">
          <v-btn id="overlayActivator" stacked height="60px" width="20px" @click="overlay = true" class="px-0">
            <template #prepend>
              <v-icon :icon="mdiPower" :size="30"></v-icon>
            </template>
            <p style="font-size: 10px; height: 25px; ">{{ t("heater.turnOnCustom") }}</p>
          </v-btn>
          <v-overlay v-model="overlay" class="align-center justify-center">
            <v-time-picker format="24hr" elevation="24" v-model:hour="hoursModel" v-model:minute="minutesModel" title="Tempo di accesione:">
              <template #actions>
                <v-btn @click="overlayOkAction">
                  <p style="font-size: 25px;">OK</p>
                </v-btn>
              </template>
            </v-time-picker>
          </v-overlay>
        </v-col>
        <v-col class="text-center">
          <v-btn stacked height="60px" width="20px" @click="turnOffHeater()" class="px-0">
            <template #prepend>
              <v-icon :icon="mdiPower" :size="30"></v-icon>
            </template>
            <p style="font-size: 10px; height: 25px; line-height: 25px;">{{ t("heater.turnOff") }}</p>
          </v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col class="text-center my-1 py-0" >
          <span>{{ t("heater.statusLabel") }}:
            <strong v-if="mainStore.isHeaterOn">{{ t("heater.status.on") }}</strong>
            <strong v-else>{{ t("heater.status.off") }}</strong>
          </span>
        </v-col>
      </v-row>
      <v-row>
        <v-col class="text-center my-1 py-0" >
          <span v-if="mainStore.isHeaterOn">
            {{ t("heater.remaining") }}: {{ remainingMinutes }}
          </span>
        </v-col>
      </v-row>
    </v-sheet>
</template>

<script setup lang="ts">
import { mdiPower } from '@mdi/js';
import { useMainStore } from '@/stores/store';
import { onMounted, ref, watch } from 'vue';
import { VTimePicker } from 'vuetify/labs/VTimePicker'

import { socket } from "@/socket";

import {useI18n} from 'vue-i18n' 


const {t} = useI18n();

const props = defineProps({
    cellHeight: { type: Number, required: true }
})

const overlay = ref(false)
const hoursModel = ref()
const minutesModel = ref()

const mainStore = useMainStore()

const remainingMinutes = ref(0)
onMounted(() => {
  socket.on("remainingHeaterMinutes", (minutes) => {
    remainingMinutes.value = minutes
  });
})

async function turnOnHeater(minutes: number) {
  
  interface serverResponse {result:string, remainingMinutes:number}
  const resp: serverResponse = await socket.emitWithAck("heaterOn", minutes)
  if(resp.result === "OK") {
    mainStore.isHeaterOn = true
    remainingMinutes.value = resp.remainingMinutes
    console.log("Heater turned on")
  }
  else {
    console.log("Heater not turned on")
  }
}

async function turnOffHeater() {
  const resp = await socket.emitWithAck("heaterOff")
  if(resp === "OK") {
    mainStore.isHeaterOn = false
    console.log("Heater turned off")
  }
  else {
    console.log("Heater not turned off")
  }
}

function overlayOkAction() {
  let totalMinutes: number = 0

  if(hoursModel.value)
    totalMinutes += hoursModel.value*60

  if(minutesModel.value)
    totalMinutes += minutesModel.value

  if(totalMinutes > 0) {
    console.log("totMinutes: ", totalMinutes)
    turnOnHeater(totalMinutes)
  }

  hoursModel.value = 0
  minutesModel.value = 0
  overlay.value = false
}




</script>