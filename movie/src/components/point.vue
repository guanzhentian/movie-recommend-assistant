<template>
	<div class="point">
		<div class="star" :style="{width: radius +'px',height:radius +'px'}">
			<img :src="pngSrc" @mouseenter = "isHover = 2"  @mouseleave = "isHover = 1" @click="isShow = !isShow" :style="{width: imgWidth +'px'}">
		</div>
		<div class="content" v-show="isShow" id="content">
			<div class="mpoint" id="mpoint">
				<div :style="{width:width,backgroundColor:bgc}" class="show"></div>
				<p class="val">{{value}}</p>
				<div class="sub" @click="submit">submit</div>
				<div class="pointer" :id="'mpoint' + movieId"></div>
			</div>	
		</div>	
	</div>
</template>
<script type="text/javascript">
	export default{
		props:{
			movieId:{
				required:true
			},
			radius:{
				default:60
			}
		},
		computed:{
			pngSrc(){
				return require('../assets/star'+this.isHover+'.png');
			},
			imgWidth(){
				return this.radius*0.8;
			}
		},
		data(){
			return{
				lastX:0,
				curX:0,
				width:'0px',
				bgc:'white',
				value:'',
				isClick:false,
				isHover:1,
				isShow:false,
				isSubmit:false
			}
		},
		mounted(){
			document.getElementById(('mpoint'+this.movieId)).addEventListener('mousedown', this.click, false)
			document.getElementById('content').addEventListener('mousemove', this.move, false)

			document.getElementById('mpoint').addEventListener('touchstart', this.touchstart, false)
			document.getElementById('content').addEventListener('touchmove', this.move, false)
		},
		methods:{
			move(e){
				if(!this.isClick)
					return
				if(e.movementX)
					this.curX += e.movementX;
				else{
					this.curX += e.touches[0].screenX - this.lastX;
					this.lastX = e.touches[0].screenX;
				}
				if(this.curX < 0)
					this.curX = 0
				else if(this.curX > 300)
					this.curX = 300
				this.value =((this.curX/300)*5).toFixed(1); 
				this.width =this.value/5*300 + 'px';
				document.getElementById(('mpoint'+this.movieId)).style.left = this.value/5*300 - 7 + 'px';
				if(this.value < 0 )
					this.value = 0;
				if(this.value >5)
					this.value  = 5;
				if(this.value < 2)
					this.bgc ='rgb(207,20,86)' ;
				else if(this.value < 3.5)
					this.bgc = 'rgb(206,207,53)';
				else
					this.bgc = 'rgb(62,203,115)';
			},
			click(e){
				this.isClick = true;
				document.addEventListener('mouseup', this.up, false)
			},
			up(){
				this.isClick = false;
				document.removeEventListener('mouseup', this.up, false)
			},
			touchstart(e){
				this.lastX = e.touches[0].screenX;
				this.isClick = true;
				document.addEventListener('touchend', this.touchend, false)
			},
			touchend(){
				this.isClick = false;
				document.removeEventListener('touchend', this.touchend, false)
			},
			submit(){
				if(this.value == '')
					return alert('请先评分！');
				this.axios.post('/userRate',{
					movieId:this.movieId,
					rate:this.value
				}).then((res)=>{
					if(res.data.status)
					{
						alert('success rate!');
						this.$emit('rating',this.movieId);
						this.isShow = false;
					}
					else
						alert('rate fail!');
					this.isSubmit = false;
				}).catch((err)=>{
					console.log(err);
					alert('rate fail!');
					this.isSubmit =false;
				})
			},
			checkLogin(){
				this.axios.get('checkLogin')
				.then((res)=>{
					if(res.data.status)
						this.submit();
					else
						alert('请先登陆！');
				})
				.catch((err)=>{
					console.log(err);
				});
			}
		}
	}
</script>
<style type="text/css" lang="less" scoped>
.point{
	display: inline-block;
	position: relative;
	.star{
		cursor: pointer;
		border-radius: 50%;
		border:1px solid #d7d7d7;
		display: flex;
		justify-content: center;
		align-items: center;
		&:hover{
			background-color: #d7d7d7;
			border-color:white;
		}
	}
	.content{
		position: absolute;
		left:-140px;
		bottom:-160px;
		width:318px;
		height:150px;
		background-color: white;
		border:1px solid #d7d7d7;
		display: flex;
		justify-content: center;
		.mpoint{
			border:1px solid #d7d7d7;
			border-radius: 10px;
			
			margin-top: 20px;
			width:300px;
			height:30px;
			background-color: white;
			position: relative;
			display: flex;
			align-items: center;
			.show{
				position: absolute;
				left:0;
				top:0;
				height:30px;
				border-radius: 10px;
			}
			.val{
				position: absolute;
				bottom:-60px;
				left:50%;
				transform: translateX(-50%);
				color:rgba(0,0,0,0.7);
			}
			.pointer{
				width:0px;
				height:0px;
				border-width: 0 7px 14px 7px;
				border-color: transparent transparent black transparent;
				border-style: solid;
				position: absolute;
				bottom:-14px;
				left:-7px;
				cursor: pointer;
			}
			.sub{
				width:100px;
				height:40px;
				line-height: 40px;
				text-align: center;
				border:1px solid #d7d7d7;
				color:black;
				border-radius:10px;
				position: absolute;
				bottom:-90px;
				cursor: pointer;
				left:50%;
				transform: translateX(-50%);
				cursor: pointer;
				&:hover{
					background-color: rgba(0,0,0,0.1);
				}
				&:active{
					background-color: rgba(0,0,0,0.2);
				}
			}
		}	
	}
}
	
</style>