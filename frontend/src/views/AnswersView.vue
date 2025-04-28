<script setup>
import {
  getFormQuestionsWithAnswersReq,
} from "@/services/api";
import { darkenHexColor, darkenHslColor, getCurrentMode, shuffleArray } from "@/services/utils";
import { ref, onMounted, computed } from "vue";
import { useI18n } from "vue-i18n";
import { useRoute } from "vue-router";

const route = useRoute();
const i18n = useI18n();

const { form } = defineProps(["form"])

const answers = ref({});

const questionTypes = [
  { name: i18n.t('forms.types.text'), value: "text" },
  { name: i18n.t('forms.types.number'), value: "number" },
  { name: i18n.t('forms.types.choice'), value: "choice" },
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

const getRandomPastelColor = () => {
  const hue = Math.floor(Math.random() * 360);
  const lightness = getCurrentMode() === 'dark' ? 60 : 80;
  return `hsl(${hue}, 70%, ${lightness}%)`; // pastel tones
}

const pastelPalette = [
  "#FFB3B3", // light red
  "#FFCC99", // peach
  "#FFFF99", // light yellow
  "#99FF99", // light green
  "#99CCFF", // light blue
  "#CC99FF", // lavender
  "#FF99CC", // light pink
  "#FFD699", // light orange
  "#B3E0FF", // sky blue
  "#E6B3FF", // light purple
  "#FF6666", // coral
  "#CCCCFF", // periwinkle
];

const getChartData = (input) => {
  if (!input) {
    return {};
  }

  const counts = {};
  input.forEach(item => {
    counts[item.text] = (counts[item.text] || 0) + 1;
  });

  const labels = Object.keys(counts);
  const data = Object.values(counts);

  let fixedColors = shuffleArray(pastelPalette);
  fixedColors = fixedColors.slice(0, labels.length);

  // if there are more labels than colors in the palette,
  // generate additional HSL pastel colors
  if (labels.length > pastelPalette.length) {
    const remainingColorsCount = labels.length - pastelPalette.length;
    const additionalColors = [];
    for (let i = 0; i < remainingColorsCount; i++) {
      additionalColors.push(getRandomPastelColor());
    }
    fixedColors = fixedColors.concat(additionalColors);
  }

  const backgroundColor = labels.map((label, index) => fixedColors[index]);
  const hoverBackgroundColor = backgroundColor.map(color => 
    color.startsWith('hsl') ? darkenHslColor(color) : darkenHexColor(color)
  );


  const chartData = {
    labels,
    datasets: [
      {
        data,
        backgroundColor,
        hoverBackgroundColor,
      },
    ],
  };
  return chartData
}

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
      <div class="w-full! flex justify-center">
        <Chart
          v-if="question.question_type === 'choice'"
          type="pie"
          :data="getChartData(answers[question.id])"
          class="w-3/5"
        />
        <DataTable
          v-else
          table-class="rounded-xl!"
          striped-rows
          :value="answers[question.id]"
          scrollable
          scroll-height="300px"
          class="w-full!"
        >
          <Column field="text" :header="$t('forms.answers')" />
          <!-- <Column field="timestamp" header="Timestamp" body-class="opacity-50" /> -->
        </DataTable>
      </div>
    </div>
  </div>
</template>
