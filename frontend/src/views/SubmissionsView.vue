<script setup>
import { getFormSubmissionsReq } from "@/services/api";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

const { form } = defineProps(['form']);

const route = useRoute();
const submissions = ref([]);

onMounted(async () => {
  try {
    const submissionsResp = await getFormSubmissionsReq(route.params.id);
    submissions.value = submissionsResp;
  } catch (e) {
    console.log(e);
  }
});
</script>
<template>
  <div class="w-full flex flex-col gap-4">
    <div
      v-for="submission in submissions"
      class="flex justify-between gap-2 bg-[var(--color-background-mute)] py-2 px-4 rounded-xl w-full!"
    >
      <div>
        <h1 class="text-2xl font-bold!">{{ $t("forms.submission") }}</h1>
        <h2 class="opacity-50">
          {{ submission.timestamp.slice(0, 10) }} {{ $t("general.at") }}
          {{ submission.timestamp.slice(11, 19) }} UTC
        </h2>
      </div>
      <RouterLink :to="`/manage/forms/${form.id}/submissions/${submission.id}`" class="flex items-center gap-2">
        <p>{{ $t('general.view') }}</p><i class="pi pi-link text-xl!"></i>
      </RouterLink>
    </div>
  </div>
</template>
