<script setup>
const props = defineProps(["id", "placeholder", "invalid", "frozen"]);
const emit = defineEmits(["input"])
const model = defineModel();
</script>
<template>
  <Textarea
    :id="props.id"
    :placeholder="props.placeholder"
    :invalid="props?.invalid"
    @input="emit('input')"
    autoResize
    rows="1"
    type="text"
    v-model="model"
    :disabled="props?.frozen"
    :class="`py-0! shadow-none! bg-transparent! outline-none! focus:outline-none! focus-visible:outline-none! px-2! rounded-md! focus:bg-[var(--color-background-highlight)]! border-none! w-full! ${props?.frozen ? '' : 'hover:bg-[var(--color-background-highlight)]!'}`"
  />
</template>
