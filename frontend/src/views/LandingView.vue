<template>
  <div class="flex flex-col w-full gap-8 md:gap-0">
  <div
    class="flex flex-col md:flex-row h-fit gap-8 md:gap-0 md:h-[70vh] w-full items-center justify-between place-content-start px-4!"
  >
    <h1 class="text-4xl md:text-5xl w-full text-center md:text-left md:w-1/3">
      {{ $t('landing.title.creating') }} <span class="font-bold!">{{ $t('landing.title.forms') }}</span> {{ $t('landing.title.hasNeverBeenThatEasy') }}
    </h1>
    <img
      src="@/assets/images/cuelandlight.png"
      alt="Example screenshot"
      class="w-full md:w-3/5 shadow-2xl shadow-indigo-900 rounded-2xl"
    />
  </div>
  <div class="flex flex-col w-full text-white bg-blue-600 px-4 md:px-6 py-4 rounded-2xl">
    <h1 class="text-5xl font-bold!">{{ $t('landing.features.features') }}</h1>
    <div class="w-full justify-between gap-4 flex flex-col md:flex-row mt-6!">
      <div class="w-full md:w-1/3 flex flex-col px-4 py-4 rounded-xl border-blue-200 border-2">
        <div class="flex gap-4 justify-start items-center mb-2!">
          <h1 class="text-6xl font-black! text-blue-200">1</h1>
          <h1 class="text-2xl/tight font-bold!">{{ $t('landing.features.first.title') }}</h1>
        </div>
        <p class="text-lg my-auto!">{{ $t('landing.features.first.text') }}</p>
      </div>
      <div class="w-full md:w-1/3 flex flex-col px-4 py-4 rounded-xl border-blue-200 border-2">
        <div class="flex gap-4 justify-start items-center mb-2!">
          <h1 class="text-6xl font-black! text-blue-200">2</h1>
          <h1 class="text-2xl/tight font-bold!">{{ $t('landing.features.second.title') }}</h1>
        </div>
        <p class="text-lg my-auto!">{{ $t('landing.features.second.text') }}</p>
      </div>
      <div class="w-full md:w-1/3 flex flex-col px-4 py-4 rounded-xl border-blue-200 border-2">
        <div class="flex gap-4 justify-start items-center mb-2!">
          <h1 class="text-6xl font-black! text-blue-200">3</h1>
          <h1 class="text-2xl/tight font-bold!">{{ $t('landing.features.third.title') }}</h1>
        </div>
        <p class="text-lg my-auto!">{{ $t('landing.features.third.text') }}</p>
      </div>
    </div>
  </div>
  </div>
  <div class="h-8"></div>
</template>
