<script setup>
import StateBadge from "@/components/StateBadge.vue";
import { useAuth } from "@/composables/useAuth";
import { getManagedFormsReq, getProfileReq } from "@/services/api";
import { copyFormLink } from "@/services/utils";
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

const router = useRouter();
const route = useRoute();
const auth = useAuth();

const profile = ref({});
const forms = ref([]);

onMounted(async () => {
  const profileData = await getProfileReq();
  profile.value = profileData;
  localStorage.setItem("username", profileData.username);

  const formsData = await getManagedFormsReq();
  forms.value = formsData;
});

const redirectToCreateForm = () => {
  router.push("/manage/forms/create");
};

const logout = () => {
  auth.logout();
  router.push("/login");
};

const copyLink = (id) => {
  copyFormLink(id);
  // PrimeVue Toasts are getting out of screen on mobile
  // toast.add({severity: 'success', summary: i18n.t('general.linkCopied'), life: 3000});
}

</script>
<template>
  <div class="flex flex-col md:w-9/10 gap-8 md:flex-row w-full justify-between">
    <div class="flex flex-col gap-4 w-full md:w-3/10">
      <h1 class="font-bold! text-3xl">{{ $t("profile.profile") }}</h1>
      <div
        class="flex flex-col p-4 gap-8 bg-[var(--color-background-soft)] rounded-2xl items-center"
      >
        <h1 class="font-bold! text-2xl text-center">{{ profile.username }}</h1>
      </div>
      <Button @click="logout" severity="danger" outlined>{{
        $t("auth.logout")
      }}</Button>
    </div>
    <div class="flex flex-col gap-4 w-full pb-4">
      <div class="flex justify-between">
        <h1 class="font-bold! text-3xl">{{ $t("forms.forms") }}</h1>
        <Button
          @click="redirectToCreateForm"
          class="py-1! items-center rounded-full! bg-[var(--color-main)]"
          >{{ $t("general.create") }} +</Button
        >
      </div>
      <div class="w-full flex flex-col gap-2">
        <RouterLink v-for="form in forms" :to="`/manage/forms/${form.id}`">
          <div class="px-4 py-2 bg-[var(--color-background-soft)] rounded-2xl">
            <div class="flex justify-between gap-4">
              <h1 class="text-xl overflow-hidden">
                <span class="mr-2! font-bold!">{{ form.title }}</span>
                <span class="font-bold! opacity-50 whitespace-nowrap">{{
                  $t("forms.questionsNumber", form.questions.length)
                }}</span>
              </h1>
              <div class="flex gap-1 items-center min-w-fit">
                <Button
                  @click.stop="copyLink(form.id)"
                  class="rounded-full! flex gap-[1px] px-2! py-0! text-nowrap max-h-fit min-h-6 min-w-10"
                  variant="outlined"
                >
                  <i class="pi pi-copy"></i>
                  <span class="hidden md:inline">{{
                    $t("general.copyLink")
                  }}</span>
                </Button>
                <StateBadge
                  :bg="
                    form.closed
                      ? 'text-white bg-red-600 dark:bg-red-700'
                      : 'text-white bg-green-600 dark:bg-green-700'
                  "
                  :text="form.closed ? $t('forms.closed') : $t('forms.active')"
                />
              </div>
            </div>
            <div class="flex gap-2">
              <p>
                {{ $t("forms.submissionsNumber", form.submission_count) }}
              </p>
            </div>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>
