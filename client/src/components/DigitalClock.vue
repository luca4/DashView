<template>

  {{ time }}

</template>

<script setup lang="ts">

  import { ref } from 'vue';

  let time = ref("")

  setInterval(updateTime, 1000);
  updateTime();

  function updateTime(): void {
      var now = new Date();
      time.value = zeroPadding(now.getHours(), 2) + ':' + zeroPadding(now.getMinutes(), 2) + ':' + zeroPadding(now.getSeconds(), 2);
  };

  function zeroPadding(num: number, digit: number): string {
      var zero = '';
      for(var i = 0; i < digit; i++) {
          zero += '0';
      }
      return (zero + num).slice(-digit);
  }

</script>