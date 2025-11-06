<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">
          <div class="nav-item">Home</div>
        </RouterLink>
        <div id="projects-nav" class="nav-item">
          Projects
          <div id="projects-dropdown" ref="projectsMenu" @click="closeProjectsMenu">
            <RouterLink to="/projects/3dprinting">
              <p>3D Printing</p>
            </RouterLink>
            <RouterLink to="/projects/photography">
              <p>Photography</p>
            </RouterLink>
            <RouterLink to="/projects/motorcycles">
              <p>Motorcycles</p>
            </RouterLink>
          </div>
        </div>
        <RouterLink to="/contact">
          <div class="nav-item">Contact Me</div>
        </RouterLink>
      </nav>
    </div>
  </header>
  <div class="content">
    <RouterView />
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {
    closeProjectsMenu() {
      // console.log("dasdasasd");
      // this.$refs.projectsMenu.style.pointerEvents = "none";
      // const style = this.$refs.projectsMenu.style.display;
      this.$refs.projectsMenu.classList.add("hidden");
      setTimeout(() => {
        this.$refs.projectsMenu.classList.remove("hidden");
      }, 5);
      // this.$refs.projectsMenu.style.display = style;
      // this.$refs.projectsMenu.style.pointerEvents = "auto";
    }
  }
};
</script>

<style lang="scss">
@import "./styles/App.scss";
</style>
