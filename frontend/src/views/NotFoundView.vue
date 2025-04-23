<template>
  <div class="flex place-content-center">
    <div>
      <h1 class="font-black! text-9xl text-center">404</h1>
      <h2 class="font-bold! text-3xl">{{ $t('general.pageNotFound') }}</h2>
      <h4 v-if="$i18n.locale == 'ru'" class="text-xl opacity-50">увы</h4>
    </div>
  </div>
</template>
