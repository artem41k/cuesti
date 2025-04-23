<script setup>
import { useAuth } from "@/composables/useAuth";
import { computed, ref } from "vue";
import { useRoute } from "vue-router";

const auth = useAuth();
const route = useRoute();

const isLanding = computed(() => {
  return route.path === '/';
})

const showLocaleSwitch = ref(false);
</script>
<template>
  <header
    class="flex items-center justify-between w-11/12 md:w-3/5 h-12 md:h-16 fixed top-4 rounded-full z-50"
  >
    <RouterLink to="/" class="flex items-center gap-4">
      <img src="@/assets/logo.svg" class="w-14 md:w-18" />
      <h1 v-if="isLanding" class="text-3xl font-bold!">cuesti</h1>
    </RouterLink>
    <nav class="flex items-center gap-4 text-base md:text-[18px]">
      <div :class="`${showLocaleSwitch ? 'hidden md:block' : 'block'}`">
        <div
          v-if="!auth.isAuthenticated()"
          class="flex items-center gap-2 text-base md:text-[18px]"
        >
          <RouterLink to="/register" class="font-black">{{
            $t("auth.register")
          }}</RouterLink>
          <div class="h-6 w-[1px] rounded-full opacity-75 bg-white"></div>
          <RouterLink to="/login">{{ $t("auth.login") }}</RouterLink>
        </div>
        <RouterLink v-else to="/profile" class="flex items-center gap-2">
          <p class="font-bold!">{{ auth.user.value?.username }}</p>
          <i class="pi pi-user"></i>
        </RouterLink>
      </div>
      <SelectButton
        v-if="showLocaleSwitch"
        @change="showLocaleSwitch = false"
        v-model="$i18n.locale"
        :options="$i18n.availableLocales"
        size="small"
        class="mx-4!"
      />
      <button
        @click="showLocaleSwitch = !showLocaleSwitch"
        class="cursor-pointer"
      >
        <i
          :class="`pi pi-globe text-xl! mt-0.5! transition-all ${
            showLocaleSwitch ? 'rotate-180' : ''
          }`"
        ></i>
      </button>
    </nav>
  </header>
</template>
<style scoped>
header {
  /* Glass effect + centering */
  padding: 0 16px !important;
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  left: 50%;
  transform: translate(-50%, 0);
}
</style>
