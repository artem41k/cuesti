<script setup>
import { computed } from 'vue';

const props = defineProps(['bg', 'text'])

</script>
<template>
  <div class="py-0.5 px-2 rounded-full min-h-4 max-h-fit" :class="props.bg">
    <span class="hidden sm:inline">{{ props.text }}</span>
  </div>
</template>