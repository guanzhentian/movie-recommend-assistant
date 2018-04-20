<template>
	<div class="mregister ">
		<div class="content">
			<h1 v-if="flag">Sign In</h1>
			<h1 v-else>Login</h1>
			<div class="input">
				<span>Name</span>
				<input type="text" v-model="name" placeholder="input your name">
			</div>
			<div class="input">
				<span>Password</span>
				<input type="password" v-model="password" placeholder="input your password">
			</div>
			<div class="input" v-if="flag">
				<span>Check Pasword</span>
				<input type="password" v-model="checkWord" placeholder="input your password agin">
			</div>
			<div class="input">
				<span>Verification code</span>
				<input type="text" v-model="yanzhengma" placeholder="input verification code">
				<canvas width="100" height="30" id="can" @click="buildYanzhenma"></canvas>
			</div>
			<div class="btn">
				<span v-if="flag">Sign In</span>
				<span v-else>Login</span>
			</div>
		</div>
	</div>
</template>
<script type="text/javascript">
	export default{
		data(){
			return{
				flag:true,
				name:'',
				password:'',
				checkWord:'',
				yanzhengma:'',
				check:''
			}
		},
		watch:{
			$route(){
				if(this.$route.path.indexOf('login') != -1)
				{
					this.flag = false;
					this.buildYanzhenma();
				}
				else
				{
					this.flag = true;
					this.buildYanzhenma();
				}
			}
		},
		methods:{
			buildYanzhenma(){
				var canvas = document.getElementById('can');
				var c = canvas.getContext('2d');
				var check = '';
				c.clearRect(0,0,100,30);
				for(var i =0;i<4;i++)
				{
					var ran = Math.random()*3;
					if(ran < 1){
						check += Math.floor(Math.random()*10)
					}
					else if(ran <2)
					{
						var ranNum = Math.floor(Math.random()*26)
						check += String.fromCharCode(65+ranNum);
					}
					else{
						var ranNum = Math.floor(Math.random()*26)
						check += String.fromCharCode(97+ranNum);
					}
				}
				c.font = '20px Arial';
				c.fillText(check,25,20);
				this.check = check;
			}
		},
		mounted(){
			if(this.$route.path.indexOf('login') != -1)
				this.flag = false;
			else
				this.flag = true;
			this.$nextTick(()=>{
				this.buildYanzhenma();
			})
		}
	}
</script>
<style type="text/css" lang="less" scoped>
	.mregister{
		background-color: #f4f4f4;
		width:100%;
		display: flex;
		justify-content: center;
		padding-top:80px;
		.content{
			color:#081c24;
			min-width: 600px;
			padding:0 20px;
			padding-bottom: 50px;
			display: flex;
			flex-direction: column;
			align-items: center;
			h1{
				margin-bottom: 50px;
			}
			.input{
				padding-bottom: 20px;
				position: relative;
				span{
					display: inline-block;
					width:150px;
				}
				input{
					border: 1px solid #d6d6d6;
					height:20px;
					padding-left: 10px;
					&:focus{
						outline: 0;
					}
				}
				canvas{
					position: absolute;
					border:1px solid #d6d6d6;
					right:-130px;
					cursor: pointer;
					top:-5px;
				}
			}
			.btn{
				font-size: 14px;
				margin-top: 50px;
				width:100px;
				height:30px;
				line-height: 30px;
				color:rgba(255,255,255,0.8);
				background-color: #081c24;
				text-align: center;
				cursor: pointer;
				border-radius: 5px;
			}
		}
	}
</style>