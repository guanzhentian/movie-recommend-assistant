<template>
	<div class="mrate" :style="{width:radius+'px',height:radius+'px'}">
		<canvas :id="'canvas' + name" :height="radius-offset" :width="radius-offset"></canvas>
		<div class="middle" v-if="persent" :style="{fontSize:fontSize+'px'}">
			{{persent}}
		</div>
	</div>
</template>
<script type="text/javascript">
	export default{
		props:{
			radius:{
				type:Number,
				default:80
			},
			value:{
				type:Number,
				default:null
			},
			total:{
				type:Number,
				default:5
			},
			fontSize:{
				type:Number,
				default:14
			},
			lineWidth:{
				type:Number,
				default:5
			},
			name:{
				required:true
			},
			offset:{
				type:Number,
				default:10
			}
		},
		data(){
			return{
				persent:null
			}
		},
		mounted(){
			var flag;
			if(this.value == null)
			{
				this.persent = 'NAN';
				flag = false;
			}else{
				this.persent =Math.round( (this.value/this.total).toFixed(2) *100);
				flag = true;
			}

			var canvas = document.getElementById('canvas'+this.name);
			var ctx = canvas.getContext('2d');
			var radius =Math.round(( this.radius - this.offset)/2 - this.lineWidth);
			var center = Math.round(( this.radius - this.offset)/2 );
			if(this.radius<80)
				console.log(radius,center)
			var color = [{
				a:62,
				b:203,
				c:115
			},{
				a:206,
				b:207,
				c:53
			},{
				a:207,
				b:20,
				c:86
			}];
			if(flag)
			{
				var i;
				console.log(this.persent);
				if(this.persent < 40)
					i = 2;
				else if(this.persent<70)
					i = 1;
				else 
					i = 0;

				ctx.beginPath();
				ctx.strokeStyle= "rgba("+color[i].a+","+color[i].b+","+color[i].c+","+"0.3)";
				ctx.arc(center,center,radius,0*Math.PI,2*Math.PI);
				ctx.lineWidth = this.lineWidth;
				ctx.stroke();
				ctx.closePath();


				ctx.beginPath();
				ctx.strokeStyle= "rgb("+color[i].a+","+color[i].b+","+color[i].c+")";
				var per = 2 * this.persent /100 + 1.5;
				ctx.arc(center,center,radius,1.5*Math.PI,per*Math.PI);
				ctx.lineWidth = this.lineWidth;
				ctx.stroke();
				ctx.closePath();
				if(this.fontSize>=10)
					this.persent+="%";

			}else{
				ctx.beginPath();
				ctx.strokeStyle= "rgb(93,93,93)";
				ctx.arc(center,center,radius,0*Math.PI,2*Math.PI);
				ctx.lineWidth = this.lineWidth;
				ctx.stroke();
				ctx.closePath();
			}
		}
	}
</script>
<style type="text/css" lang="less" scoped>
	.mrate{
		border-radius: 50%;
		background-color: #081c22;
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
		.middle{
			position: absolute;
			left:50%;
			top:50%;
			transform: translate(-50%,-50%);
			color:white;
		}
	}
</style>