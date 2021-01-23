<template>
  <div class="add-new">
    <img src="../../assets/plus.png" alt="add"/>
    <p> Dodaj nowy</p>
  </div>
</template>

<script>
export default {
  name: "AddNew"
}
</script>

<style scoped lang="scss">
.add-new {
  height: 60px;
  display: flex;
  align-items: center;
  width: 200px;
  border: solid 2px var(--border-color-1);
  margin-bottom: 30px;
  transition: all .3s ease-in-out;
  cursor: pointer;

img {
  height: 100%;
  filter: invert(96%) sepia(10%) saturate(1236%) hue-rotate(61deg) brightness(99%) contrast(88%);
}

p {
  margin-left: 15px;
}

&:hover{
   background-color: var(--bg-block-hover);
 }
}
</style>