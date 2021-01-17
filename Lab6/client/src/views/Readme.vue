<template>
	<v-container>
		<v-card max-width="500" class="mx-auto">
			<v-card-text><editor v-model="content" mode="viewer"/></v-card-text>
		</v-card>
	</v-container>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { Editor } from "vuetify-markdown-editor";
import readmeContent from "@/../../README.md";

@Component({
	components: {
		Editor
	}
})
export default class Readme extends Vue {
	get content() {
		return readmeContent;
	}
}
</script>
