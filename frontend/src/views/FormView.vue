<script setup>
import { getFormReq, submitFormReq } from "@/services/api";
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const form = ref({});

const answers = ref({});
const success = ref(false);
const err = ref("");

onMounted(async () => {
  // form.value = test;
  try {
    const formData = await getFormReq(route.params.id);
    form.value = formData;
  } catch (e) {
    console.log(e);
  }
});

const submit = async () => {
  const data = { answers: answers.value };
  try {
    const response = await submitFormReq(route.params.id, data);
    success.value = true;
  } catch (e) {
    const errData = e?.response?.data;
    console.log(errData);
    if (errData.constructor === Array) {
      if (errData[0]?.non_field_errors) {
        err.value = errData[0].non_field_errors[0];
      } else {
        err.value = errData[0];
      }
    } else {
      err.value = "Something went wrong";
    }
  }
};
</script>
<template>
  <div
    class="flex flex-col w-full md:w-7/10 gap-2 md:gap-4 bg-[var(--color-background-soft)] rounded-2xl md:rounded-4xl px-2 py-2 md:px-8 md:py-4"
  >
    <div>
      <h1 class="font-bold! text-2xl md:text-3xl mx-2!">{{ form.title }}</h1>
      <p class="text-xl mx-2! mt-2!">{{ form.description }}</p>
    </div>
    <div v-if="!success" class="w-full flex flex-col gap-4">
      <div
        v-for="question in form.questions"
        class="bg-[var(--color-background-mute)] py-2 px-4 rounded-xl"
      >
        <div class="flex justify-between gap-2">
          <h2 class="font-bold! text-lg md:text-xl">{{ question.title }}</h2>
          <p class="text-red-700" v-if="question.required">{{ $t('forms.required') }}</p>
        </div>
        <p class="opacity-75">{{ question.description }}</p>
        <Textarea
          v-if="question.question_type === 'text'"
          class="mt-2! w-full md:w-full -mb-2!"
          v-model="answers[question.id]"
          :id="question.id"
          :placeholder="$t(`forms.types.${question.question_type}`)"
          :maxlength="question.max_length ? question.max_length : ''"
          autoResize
          rows="1"
        />
        <InputNumber
          v-if="question.question_type === 'number'"
          class="mt-2! w-full md:w-full"
          v-model="answers[question.id]"
          :max-fraction-digits="question.is_float ? 2 : 0"
          :min="question.min_value ? question.min_value : undefined"
          :max="question.max_value ? question.max_value : undefined"
          :id="question.id"
          :placeholder="$t(`forms.types.${question.question_type}`)"
        />
        <div v-if="question.question_type === 'choice'" class="mt-2! flex flex-col gap-1">
          <div
            v-for="choice in question.choices"
            class="flex gap-2 rounded-xl w-full py-1 px-2 items-center cursor-pointer"
            :class="answers[question.id] === choice.answer ? 'bg-[var(--color-background-highlight)]': ''"
            @click="answers[question.id] = choice.answer"
          >
            <RadioButton @click.stop :value="choice.answer" v-model="answers[question.id]" />
            <p>{{ choice.answer }}</p>
          </div>
        </div>
        <div class="opacity-75 ml-2!">
          <!-- Number -->
          <small v-if="question.max_value != null && question.min_value != null">
            {{ $t("general.fromAToB", {a: question.min_value, b: question.max_value}) }}
          </small>
          <small v-else-if="question.max_value != null">
            {{ $t("general.max", question.max_value) }}
          </small>
          <small v-else-if="question.min_value != null">
            {{ $t("general.min", question.min_value) }}
          </small>
          <!-- Text -->
          <small v-else-if="question.max_length != null">
            {{ $t("general.maxChar", question.max_length) }}
          </small>
        </div>
      </div>

      <Button @click="submit" type="submit" class="w-full rounded-xl!"
        >{{ $t('general.submit') }}</Button
      >
      <!-- <p>{{ answers }}</p> -->
      <p class="text-red-700" v-if="err">{{ err }}</p>
    </div>
    <div v-else class="bg-green-300 dark:bg-green-700 py-2 px-4 rounded-xl">
      <p>{{ $t("forms.formSuccessfullySubmitted") }}</p>
    </div>
  </div>
</template>
