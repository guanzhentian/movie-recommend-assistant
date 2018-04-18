<template>
	<div class="mfoot" >
		<div class="mfcontent">
			<div class="mfmain">
				<h1>LOGO</h1>
				<div>
					<h1>官少</h1>
				</div>	
			</div>
			
		</div>
	</div>
</template>
<script type="text/javascript">
	export default{
		data(){
			return{
				bg:require('../assets/1.jpg'),
			}
		},
	}
</script>
<style type="text/css" scoped lang="less">
	.mfoot{
		background-position: center;
		background-size: cover;
		width: 100%;
		.mfcontent{
			width: 100%;
			height:100%;
			display: flex;
			justify-content: center;
			.mfmain{
				color:#081c24;
				width:1200px;
				padding:0 20px;
				display: flex;
				justify-content: space-between;
				align-items: center;
				height:150px;	
			}
			
		}
	}
</style>