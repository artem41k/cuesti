<script setup>
import { getFormReq, getManagedFormReq, getSubmissionReq } from "@/services/api";
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

const form = ref({});
const submission = ref({});

const route = useRoute();

onMounted(async () => {
  try {
    const formData = await getManagedFormReq(route.params.id);
    form.value = formData;
    const submissionData = await getSubmissionReq(route.params.id, route.params.subId);
    submission.value = submissionData;
  } catch (e) {
    console.log(e);
  }
});

const getAnswer = (qId) => {
  if (!submission.value || !form.value) {
    return null;
  }
  return submission.value.answers.find((ans) => ans.question.id == qId)
}

</script>
<template>
  <div
    class="flex flex-col w-full md:w-7/10 gap-2 md:gap-4 bg-[var(--color-background-soft)] rounded-2xl md:rounded-4xl px-2 py-2 md:px-8 md:py-4"
  >
    <div>
      <h1 class="font-bold! text-2xl md:text-3xl mx-2!">{{ form.title }}</h1>
      <p class="text-xl mt-2!">{{ form.description }}</p>
    </div>
    <div class="w-full flex flex-col gap-4">
      <div
        v-for="question in form.questions"
        class="bg-[var(--color-background-mute)] py-2 px-4 rounded-xl"
      >
        <div class="flex justify-between gap-2">
          <h2 class="font-bold! text-lg md:text-xl">{{ question.title }}</h2>
          <p class="text-red-700" v-if="question.required">{{ $t('forms.required') }}</p>
        </div>
        <p class="opacity-75">{{ question.description }}</p>
        <div v-if="getAnswer(question.id)" class="my-2! bg-[var(--color-background-highlight)] py-2 px-4 rounded-xl">
            <p>{{ getAnswer(question.id)?.text }}</p>
        </div>
        <p v-else class="opacity-50">{{ $t('forms.noAnswer') }}</p>
      </div>
    </div>
  </div>
</template>
