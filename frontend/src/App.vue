<script setup>
import { useRoute } from "vue-router";
import AppHeader from "@/components/AppHeader.vue";
import { computed, onMounted } from "vue";
import { eventBus } from "./services/eventBus";
import { useAuth } from "./composables/useAuth";

const auth = useAuth();
const route = useRoute();

onMounted(() => {
  eventBus.onLogout = auth.logout;
});

const headerHidden = computed(() => {
  return route.path.includes("/f/") && !auth.isAuthenticated;
});

const smallScreenMargin = computed(() => {
  return headerHidden.value ? "mt-6!" : "mt-26!";
});
</script>

<template>
  <Toast />
  <AppHeader v-if="!headerHidden" />
  <main
    :class="`w-full px-2 ${smallScreenMargin} md:mt-26! md:px-16 flex flex-col items-center justify-center`"
  >
    <RouterView />
  </main>
  <AppFooter v-if="route.path === '/'" />
</template>
