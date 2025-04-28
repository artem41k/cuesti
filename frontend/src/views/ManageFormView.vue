<script setup>
import { useAuth } from "@/composables/useAuth";
import {
  deleteFormReq,
  getFormQuestionsWithAnswersReq,
  getManagedFormReq,
} from "@/services/api";
import { copyFormLink } from "@/services/utils";
import { useConfirm, useToast } from "primevue";
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { useRoute, useRouter } from "vue-router";
import AnswersView from "./AnswersView.vue";
import SubmissionsView from "./SubmissionsView.vue";

const auth = useAuth();
const route = useRoute();
const router = useRouter();
const confirm = useConfirm();
const toast = useToast();
const i18n = useI18n();

const form = ref({});

const answers = ref({});

const sections = [
  {name: i18n.t('forms.byQuestions'), value: 'byQuestions'},
  {name: i18n.t('forms.bySubmissions'), value: 'bySubmissions'},
]

const currentSection = ref("byQuestions");

onMounted(async () => {
  auth.fetchUser();
  try {
    const formData = await getManagedFormReq(route.params.id);
    form.value = formData;
    const formAnswers = await getFormQuestionsWithAnswersReq(route.params.id);
    answers.value = formAnswers;
  } catch (e) {
    console.log(e);
  }
});

const confirmDelete = () => {
    confirm.require({
        message: i18n.t('forms.confirmDelete'),
        header: i18n.t('forms.delete'),
        icon: 'pi pi-trash',
        rejectLabel: i18n.t('general.cancel'),
        rejectProps: {
            label: i18n.t('general.cancel'),
            severity: 'secondary',
            outlined: true
        },
        acceptProps: {
            label: i18n.t('general.delete'),
            severity: 'danger'
        },
        accept: () => {
          try {
            const response = deleteFormReq(form.value.id);
            router.push('/profile');
          } catch (e) {
            console.log(e?.response?.data)
          }
        },
        reject: () => {}
    });
};

const copyLink = () => {
  copyFormLink(form.value.id);
  // PrimeVue Toasts are getting out of screen on mobile
  // toast.add({severity: 'success', summary: i18n.t('general.linkCopied'), life: 3000, styleClass: 'max-w-screen'});
}

const downloadExcel = () => {
  window.location.href = `/api/manage/forms/${form.value.id}/excel`;
}

</script>
<template>
  <ConfirmDialog class="mx-2!" />
  <div class="flex w-full mb-8!">
    <div class="flex flex-col w-full gap-2">
      <div
        class="flex flex-col w-full! md:w-4/5 gap-4 bg-[var(--color-background-soft)] rounded-4xl px-4 py-4 md:px-8 md:py-4"
      >
        <div class="flex gap-4 justify-between">
          <div>
            <h1 class="font-bold! text-2xl md:text-3xl">{{ form.title }}</h1>
            <p class="text-xl mt-2!">{{ form.description }}</p>
          </div>
          <div class="flex gap-1">
            <Button
              @click="downloadExcel"
              class="rounded-full! flex gap-[1px] px-2! py-0! text-nowrap max-h-fit min-h-6 min-w-10"
              severity="success"
            >
              <i class="pi pi-table"></i>
              <span class="hidden md:inline">{{ $t("general.downloadTable") }}</span>
            </Button>
            <Button
              @click="copyLink"
              class="rounded-full! flex gap-[1px] px-2! py-0! text-nowrap max-h-fit min-h-6 min-w-10"
            >
              <i class="pi pi-copy"></i>
              <span class="hidden md:inline">{{ $t("general.copyLink") }}</span>
            </Button>
            <Button
              @click="confirmDelete"
              severity="danger"
              class="rounded-full! flex gap-[1px] px-2! py-0! text-nowrap max-h-fit min-h-6 min-w-10"
            >
              <i class="pi pi-trash"></i>
              <span class="hidden md:inline">{{ $t("general.delete") }}</span>
            </Button>
          </div>
        </div>
        <SelectButton size="large" :options="sections" v-model="currentSection" option-label="name" option-value="value" />
        <AnswersView v-if="currentSection === 'byQuestions'" :form="form" />
        <SubmissionsView v-if="currentSection === 'bySubmissions'" :form="form" />
      </div>
    </div>
  </div>
</template>
