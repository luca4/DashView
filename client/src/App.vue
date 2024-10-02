<template>

<v-app>

  <v-app-bar density="compact" absolute :elevation="2" class="bg-indigo-darken-4">

    <v-app-bar-title >
      <AppBar />
    </v-app-bar-title>
  </v-app-bar>

  <v-main class="bg-indigo-darken-3">
    
    <v-row style="height: 50%;" no-gutters align="center">
    
      <v-col >
        <HeaterBlock :cellHeight=cellsHeight />
      </v-col >
    
      <v-col>
        <AmbientDataBlock :cellHeight=cellsHeight />
      </v-col>
    
      <v-col>
        <TrashBlock :cellHeight=cellsHeight />
      </v-col>
    
    </v-row>
  
    <v-row style="height: 50%;" no-gutters align="center">
    
      <v-col >
        <v-sheet class="pa-2 ma-3 rounded-lg" :height="cellsHeight">
          <v-chip prepend-icon="$vuetify">
            Eventi - calendar
          </v-chip>
        </v-sheet>
      </v-col >
    
      <v-col>
        <v-sheet class="pa-2 ma-3 rounded-lg" :height="cellsHeight">
          <v-chip prepend-icon="$vuetify">
            panneli solari
          </v-chip>
        </v-sheet>
      </v-col>
    
      <v-col>
        <v-sheet class="pa-2 ma-3 rounded-lg" :height="cellsHeight">
          <v-chip prepend-icon="$vuetify">
            luci
          </v-chip>
        </v-sheet>
      </v-col>
      
    </v-row>

  </v-main>

</v-app>


</template>

<script setup lang="ts">
  import AppBar from './components/AppBar.vue';
  import { onMounted } from 'vue';
  import { useConnectionStore } from "@/stores/connectionStore";
  import { socket } from './socket';

  // Blocks
  import HeaterBlock from './components/Blocks/HeaterBlock.vue'
  import AmbientDataBlock from './components/Blocks/AmbientDataBlock.vue';
  import TrashBlock from './components/Blocks/TrashBlock.vue';

  const cellsHeight:number = 155;

  onMounted(() => {
    const connectionStore = useConnectionStore();

    socket.off();
    connectionStore.bindEvents();
    connectionStore.connect();

  })

</script>
