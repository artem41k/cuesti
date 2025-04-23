<script setup>
import TransparentInput from "@/components/TransparentInput.vue";
import { useAuth } from "@/composables/useAuth";
import { createFormReq } from "@/services/api";
import { copyFormLink } from "@/services/utils";
import { computed, onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";

const auth = useAuth();
const i18n = useI18n();

const form = ref({});
const questions = ref([{ internalId: 0, required: false }]);
const invalid = ref({
  formTitle: false,
  titles: [],
  types: [],
});
const success = ref(false);
const response = ref({});

onMounted(() => {
  auth.fetchUser();
  form.value = JSON.parse(localStorage.getItem('rawCreateFormData')) || {};
  questions.value = JSON.parse(localStorage.getItem('rawCreateQuestionsData')) || [{ internalId: 0, required: false }];
})

const questionTypes = [
  { name: i18n.t('forms.text'), value: "text" },
  { name: i18n.t('forms.number'), value: "number" },
  // TODO
  // { name: "Color", value: "color" },
];

const validateTitle = () => {
  if (!form.value?.title) {
    invalid.value.formTitle = true;
  } else {
    invalid.value.formTitle = false;
  }
};

const validateQuestion = (question) => {
  const intId = question.internalId;
  if (!question?.title) {
    if (!(intId in invalid.value.titles)) {
      invalid.value.titles = [intId, ...invalid.value.titles];
    }
  } else {
    invalid.value.titles = invalid.value.titles.filter((v) => v !== intId);
  }
  if (!question?.question_type) {
    if (!(intId in invalid.value.types)) {
      invalid.value.types = [intId, ...invalid.value.types];
    }
  } else {
    invalid.value.types = invalid.value.types.filter((v) => v !== intId);
  };
  localStorage.setItem('rawCreateFormData', JSON.stringify(form.value));
  localStorage.setItem('rawCreateQuestionsData', JSON.stringify(questions.value));
};

const validateForm = () => {
  validateTitle();
  questions.value.forEach((q) => {
    validateQuestion(q);
  });
};

const formValid = computed(() => {
  const inv = invalid.value;
  return !inv.formTitle && !inv.titles.length && !inv.types.length && questions.value.length > 0;
});

const addQuestion = () => {
  const lastEl = questions.value.at(-1);
  questions.value.push({
    internalId: (lastEl ? lastEl.internalId : 0) + 1,
    required: false,
  });
};
const deleteQuestion = (dq) => {
  questions.value = questions.value.filter(
    (q) => q.internalId !== dq.internalId
  );
};

const getFullFormData = computed(() => {
  return {
    ...form.value,
    // map removes internalId from question objects
    questions: questions.value.map((question) => {
      const { internalId, ...newQuestion } = question;
      return newQuestion;
    }),
  };
});

const createForm = async () => {
  validateForm();
  const validationResult = formValid.value;
  if (validationResult === true) {
    const responseData = await createFormReq(getFullFormData.value);
    response.value = responseData;
    success.value = true;
    localStorage.removeItem('rawCreateFormData');
    localStorage.removeItem('rawCreateQuestionsData');
  }
};

const copyLink = () => {
  copyFormLink(response.value.id);
  // PrimeVue Toasts are getting out of screen on mobile
  // toast.add({severity: 'success', summary: i18n.t('general.linkCopied'), life: 3000});
}

</script>
<template>
  <div
    class="flex flex-col w-full md:w-4/5 gap-4 bg-[var(--color-background-soft)] rounded-4xl px-4 py-4 md:px-8 md:py-4"
  >
    <div class="w-full flex flex-col gap-1 md:gap-2">
      <TransparentInput
        class="font-bold! text-2xl! md:text-3xl!"
        :placeholder="$t('forms.title')"
        id="formTitle"
        v-model="form.title"
        :invalid="invalid.formTitle"
        :frozen="success"
        @input="validateTitle"
      />
      <TransparentInput
        class="text-lg! md:text-xl!"
        :placeholder="$t('forms.description')"
        id="formDescription"
        v-model="form.description"
        :frozen="success"
      />
    </div>
    <div v-if="!success" class="w-full flex flex-col gap-4">
      <div
        v-for="question in questions"
        class="bg-[var(--color-background-mute)] flex flex-col gap-4 py-2.5 px-3 rounded-2xl"
      >
        <div class="flex flex-col gap-1 content-center">
          <div class="flex flex-col-reverse md:flex-row justify-between items-start gap-2">
            <TransparentInput
              class="font-bold! text-lg! md:text-xl!"
              :placeholder="$t('forms.question')"
              id="qTitle"
              v-model="question.title"
              @input="validateQuestion(question)"
              :invalid="question.internalId in invalid.titles"
            />
            <div class="flex w-full justify-between md:w-fit self-end items-center gap-2 md:gap-4">
              <button
                v-if="question?.required"
                @click="question.required = false"
                class="px-2 rounded-full border-1 border-red-500 dark:border-red-900 cursor-pointer"
              >
                <p class="text-red-500 dark:text-red-700">
                  {{ $t("forms.required") }}
                </p>
              </button>
              <button
                v-else
                @click="question.required = true"
                class="px-2 rounded-full border-1 border-gray-300 dark:border-gray-600 cursor-pointer"
              >
                <p class="text-gray-500 whitespace-nowrap">
                  {{ $t("forms.notRequired") }}
                </p>
              </button>
              <i
                @click="deleteQuestion(question)"
                class="pi pi-times text-base! cursor-pointer"
              ></i>
            </div>
          </div>
          <TransparentInput
            class="opacity-75"
            :placeholder="$t('forms.description').toLowerCase()"
            id="qDesc"
            v-model="question.description"
          />
        </div>
        <Select
          v-model="question.question_type"
          :options="questionTypes"
          option-label="name"
          option-value="value"
          :placeholder="$t('forms.selectQuestionType')"
          @value-change="validateQuestion(question)"
          :invalid="question.internalId in invalid.types"
          class="py-0!"
        />
        <Accordion v-if="question?.question_type && question?.question_type !== 'color'" value="0">
          <AccordionPanel class="border-none!">
            <AccordionHeader
              class="bg-transparent! py-0! px-2! gap-2! justify-start!"
            >
              <div class="ml-2 self-start flex gap-1 items-center">
                <span>{{ $t("forms.restrictionsLabel") }}</span>
              </div>
            </AccordionHeader>
            <AccordionContent class="pt-2 px-0!">
              <div
                v-if="question.question_type == 'text'"
                class="flex flex-col sm:flex-row gap-4"
              >
                <div class="flex flex-col gap-1">
                  <h1 class="font-semibold!">
                    {{ $t("forms.restrictions.maxAnswerLength") }}
                  </h1>
                  <InputNumber v-model="question.max_length" :placeholder="$t('placeholders.number')" fluid />
                </div>
                <div class="flex flex-col gap-1">
                  <h1 class="font-semibold!">
                    {{ $t("forms.restrictions.regex") }}
                  </h1>
                  <InputText v-model="question.regex" :placeholder="$t('placeholders.regex')" fluid />
                </div>
              </div>
              <div
                v-if="question.question_type == 'number'"
                class="flex flex-col sm:flex-row gap-4"
              >
                <div class="flex flex-col gap-1">
                  <h1 class="font-semibold!">
                    {{ $t("forms.restrictions.minValue") }}
                  </h1>
                  <InputNumber
                    v-model="question.min_value"
                    :maxFractionDigits="2"
                    :placeholder="$t('placeholders.number')"
                    fluid
                  />
                </div>
                <div class="flex flex-col gap-1">
                  <h1 class="font-semibold!">
                    {{ $t("forms.restrictions.maxValue") }}
                  </h1>
                  <InputNumber
                    v-model="question.max_value"
                    :maxFractionDigits="2"
                    :placeholder="$t('placeholders.number')"
                    fluid
                  />
                </div>
                <div class="flex flex-col gap-1">
                  <h1 class="font-semibold!">{{ $t('forms.restrictions.numericAnswerType') }}</h1>
                  <div class="flex items-center gap-2">
                    <Checkbox v-model="question.is_float" binary />
                    <p>{{ $t("forms.restrictions.canBeFloat") }}</p>
                  </div>
                </div>
              </div>
            </AccordionContent>
          </AccordionPanel>
        </Accordion>
      </div>
      <button
        @click="addQuestion"
        class="bg-[var(--color-background-mute)] py-2 px-4 rounded-full cursor-pointer"
      >
        <span class="text-md font-semibold! text-center"
          >{{ $t("forms.addQuestion") }} +</span
        >
      </button>
      <Button
        @click="createForm"
        :disabled="!formValid"
        type="submit"
        class="w-full rounded-xl!"
        >{{ $t("general.create") }}</Button
      >
    </div>
    <div v-else class="flex flex-col gap-4">
      <div class="bg-green-300 dark:bg-green-700 py-2 px-4 rounded-xl">
        <p class="text-base">{{ $t("forms.formSuccessfullyCreated") }}</p>
      </div>
      <div class="flex justify-between gap-2">
        <p class="text-base">{{ $t("forms.nowYouCanShareViaLink") }}</p>
        <Button
          @click="copyLink"
          class="rounded-full! flex gap-[1px] px-2! py-0! text-nowrap max-h-fit min-h-6 min-w-10"
        >
          <i class="pi pi-copy"></i>
          <p class="hidden md:inline">{{ $t("general.copyLink") }}</p>
        </Button>
      </div>
    </div>
  </div>
</template>
<style scoped>
:root {
  --p-accordion-content-background: var(--color-text) !important;
}
</style>
