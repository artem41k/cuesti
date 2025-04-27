<script setup>
import {
  getFormQuestionsWithAnswersReq,
} from "@/services/api";
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { useRoute } from "vue-router";

const route = useRoute();
const i18n = useI18n();

const { form } = defineProps(["form"])

const answers = ref({});

const questionTypes = [
  { name: i18n.t('forms.text'), value: "text" },
  { name: i18n.t('forms.number'), value: "number" },
  // TODO
  // { name: "Color", value: "color" },
];

onMounted(async () => {
  try {
    const formAnswers = await getFormQuestionsWithAnswersReq(route.params.id);
    answers.value = formAnswers;
  } catch (e) {
    console.log(e);
  }
});

</script>
<template>
  <div class="w-full flex flex-col gap-4">
    <div
      v-for="question in form.questions"
      class="flex flex-col md:flex-row justify-between gap-2"
    >
      <!-- Question -->
      <div
        class="bg-[var(--color-background-mute)] py-2 px-4 rounded-xl w-full!"
      >
        <div class="flex justify-between gap-2">
          <h2 class="font-bold! text-lg md:text-xl">{{ question.title }}</h2>
          <p class="text-red-700" v-if="question.required">
            {{ $t("forms.required") }}
          </p>
        </div>
        <p class="opacity-75">
          {{ question.description }}
        </p>
        <Select
          class="mt-2! w-full md:w-full"
          :model-value="question.question_type"
          :options="questionTypes"
          option-label="name"
          option-value="value"
          disabled
        />
      </div>
      <!-- Answers -->
      <div class="w-full!">
        <DataTable
          table-class="rounded-xl!"
          striped-rows
          :value="answers[question.id]"
          scrollable
          scroll-height="300px"
        >
          <Column field="text" :header="$t('forms.answers')" />
          <!-- <Column field="timestamp" header="Timestamp" body-class="opacity-50" /> -->
        </DataTable>
      </div>
    </div>
  </div>
</template>
