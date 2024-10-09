<template>
    <v-sheet class="pa-0 ma-3 rounded-lg" :height="cellHeight">
      <v-row no-gutters>
        <v-col class="text-center">
          <p class="mt-n5 mb-3 text-white" style="font-size: 14px; height: 18px; ">{{ t("trash.trashLabel") }}</p>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col class="text-center mt-4" >
          <p style="font-size: 20px;">{{ t("trash.today") }}: {{ todayTrash }}</p>     
        </v-col>
      </v-row>
      <v-row>
        <v-col class="text-center my-0" >
          <p style="font-size: 20px;">{{ t("trash.tomorrow") }}: {{ tomorrowTrash }}</p>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col class="text-right">
          <v-btn id="trashSetupBtn" density="compact" class="px-0 mx-0 mt-3 mr-1"  text="setup"></v-btn>
        </v-col>
      </v-row>
      <v-overlay activator="#trashSetupBtn" class="align-center justify-center">
        <v-sheet class="pa-4 rounded-lg">
          <v-container>
            <v-row>
              <v-col class="text-center">
                <p style="font-size: 18px;"><strong>{{ t("trash.trashDatabase") }}</strong></p>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="text-center">
                <p>{{ t("trash.lastUpdate") }}: {{ lastTrashDbUpdate }}</p>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="text-center my-0">
                <v-btn @click="updateTrashDb">{{ t("trash.updateNow") }}</v-btn>
              </v-col>
              <v-col v-if="isTrashDbUpdating">
                <v-progress-circular color="primary" indeterminate>
                </v-progress-circular>
              </v-col>
            </v-row>
          </v-container>
        </v-sheet>
      </v-overlay>
      <v-snackbar v-model="snackbarOk" :timeout="2000" color="success" rounded="pill" class="text-center">
        <p style="font-size: 18px;">{{ t("trash.dbUpdateSuccess") }}</p>
      </v-snackbar>
      <v-snackbar v-model="snackbarFail" :timeout="2000" color="error" rounded="pill" class="text-center">
        <p style="font-size: 18px;">{{ t("trash.dbUpdateFailure") }}</p>
      </v-snackbar>
    </v-sheet>
</template>

<script setup lang="ts">

import { socket } from "@/socket";
import { onMounted, ref } from 'vue';

import {useI18n} from 'vue-i18n' 


const {t} = useI18n();

const props = defineProps({
    cellHeight: { type: Number, required: true }
})

const todayTrash = ref("--")
const tomorrowTrash = ref("--")
const lastTrashDbUpdate = ref("")

const snackbarOk = ref(false)
const snackbarFail = ref(false)

const isTrashDbUpdating = ref(false)

onMounted(async () => {

  // Register for trash data events emitted from server
  socket.on("trashData", (data: {today:Array<string>, tomorrow:Array<string>}) => {
    setTrashData(data)
  });

  // Once created ask for trash data
  interface serverResponse {today:any, tomorrow:any, result:string, lastDbUpdate:any}
  const resp: serverResponse = await socket.emitWithAck("getTrash")
  setTrashData({today:resp.today, tomorrow:resp.tomorrow})

  // Once created set last update time
  lastTrashDbUpdate.value = new Date(resp.lastDbUpdate).toLocaleString()
})

// Set trash data shown
function setTrashData(data: {today:Array<string>, tomorrow:Array<string>}) {
  todayTrash.value = data.today.length == 0 ? "--" : data.today.join(", ")
  tomorrowTrash.value = data.tomorrow.length == 0 ? "--" : data.tomorrow.join(", ")
}

// Ask to server to update trash db and refresh update time and trash data shown
async function updateTrashDb() {
  isTrashDbUpdating.value = true

  interface serverResponse {today:any, tomorrow:any, result:string, lastDbUpdate:any}
  const resp: serverResponse = await socket.emitWithAck("updateTrashDb")

  if(resp.result === "OK") {
    setTrashData({today:resp.today, tomorrow:resp.tomorrow})

    const lastDbUpdate = new Date(resp.lastDbUpdate)
    lastTrashDbUpdate.value = lastDbUpdate.toLocaleString()

    snackbarOk.value = true
  }
  else {
    snackbarFail.value = true
  }

  isTrashDbUpdating.value = false
}

</script>