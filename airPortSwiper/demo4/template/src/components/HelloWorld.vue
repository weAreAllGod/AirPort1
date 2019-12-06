<template>
<body>

<h1 style="margin-top:5px;text-align:center"> 航班信息预览表</h1>
<label>最近更新时间：{{upDataTime}}</label>
<div id="list-complete-demo" class="demo">
    <div class="tablediv" >
    <!-- <label>滚动速度（单位：秒）</label>
    <select v-model="optionValue" style="width:100px"> 
      <option  disabled value="0">请选择</option>
      <option v-for="(item,index) in selectList" :key="index" :value="index+1" >
        {{item}}
      </option> 
    </select> -->
   
    <input v-on:click="test" type="button"  value="确定"> 
    
    <table class="table table-hover" style=" margin-bottom: 0rem;text-align: center">
      
        <thead >    
            <tr >                
            <th>到达时间</th>
            <th>进港航班号</th>   
            <th>起始地</th>
            <th>起飞时间</th>
            <th>出港航班号</th>  
            <th>目的地</th>
            <th>机号</th>  
            <th>机型</th>
            <th>属性</th>  
            <th>航班状态</th>
            <th>公务机</th>  
            <th>VIP</th>
            <th>已分配停机位</th>       
            <th>结果状态</th>
            <th>新分配停机位</th>  
          
              
            
            </tr>
        </thead> 
        <tbody >          
        <!-- class="list-complete-item" -->
        <!-- <transition-group name="list-complete" tag="p"> -->
        <tr v-for="(value,index) in items " :key="index"  > 

<td>{{value.atime}}</td>
<td>{{value.aflightno}}</td>
  <td>{{value.Forg}}</td>
  <td>{{value.dtime}}</td>
 <td>{{value.dflightno}}</td>
 <td>{{value.Fest}}</td>
 <td>{{value.planeno}}</td>
  <td>{{value.mdl}}</td>
  <td>{{value.nation}}</td>       
  <td>{{value.business}}</td>         
  <td>{{value.paras}}</td>    
   <td>{{value.IsVip}}</td>          
  <td>{{value.ParkingGate}}</td>  
  <td>{{value.resulttype}}</td>        
  <td>{{value.result}}</td>
  </tr>
        <!-- </transition-group> -->
      </tbody>
    </table>
    </div >
     <!-- <div class="tablediv1"> 
     <table class="table table-hover" style="text-align: center">
        
     </table>
     </div> -->
</div>

</body>
</template>
<script>

import '../../static/loadsh.js'
import { clearInterval } from 'timers';
// import axios from 'axios'

export default {
    name:"Home",
    data() {
    return {
      optionValue:0,
      selectList:[0.5,1,1.5,2,2.5,5],
      speedInput:"1.5",
      setInterval1:0,
      upDataTime:"2019-06-28 14:54:26",

      items:[
       {
				mdl: "B737",
				planeno: "B5231",
				Forg: "昆明",
				nation: "1",
				atime: "2018-10-31 19:08:00",
				business: "0",
				result: null,
				Fest: "昆明",
				dtime: "2018-11-01 07:56:00",
				paras: "0",
				aflightno: "MU5925",
				dflightno: "MU5735",
				IsVip: false,
				ParkingGate: "2",
				resulttype: null
        }, {
          mdl: "B737",
          planeno: "B5255",
          Forg: "重庆",
          nation: "1",
          atime: "2018-10-31 19:50:00",
          business: "0",
          result: null,
          Fest: "重庆",
          dtime: "2018-11-01 07:39:00",
          paras: "0",
          IsVip: false,
          ParkingGate: "1",
          resulttype: null
        }, {
          mdl: "A319",
          planeno: "B6210",
          Forg: "南宁",
          nation: "1",
          atime: "2018-10-31 23:02:00",
          business: "0",
          result: null,
          Fest: "贵阳",
          dtime: "2018-11-01 07:22:00",
          paras: "0",
          aflightno: "JD5750",
          dflightno: "JD5637",
          IsVip: false,
          ParkingGate: "12",
          resulttype: null
        }, {
          mdl: "A320",
          planeno: "B1621",
          Forg: "石家庄",
          nation: "1",
          atime: "2018-10-31 23:47:00",
          business: "0",
          result: null,
          Fest: "长沙",
          dtime: "2018-11-01 07:49:00",
          paras: "0",
          aflightno: "JD5658",
          dflightno: "JD5189",
          IsVip: false,
          ParkingGate: "14",
          resulttype: null
        }, {
          mdl: "A320",
          planeno: "B6867",
          Forg: "浦东",
          nation: "1",
          atime: "2018-10-31 23:58:00",
          business: "0",
          result: null,
          Fest: "合肥",
          dtime: "2018-11-01 08:29:00",
          paras: "0",
          aflightno: "JD5666",
          dflightno: "JD5245",
          IsVip: false,
          ParkingGate: "10",
          resulttype: null
        }, {
				mdl: "B737",
				planeno: "B5292",
				Forg: "绵阳",
				nation: "1",
				atime: "2018-11-01 00:06:00",
				business: "0",
				result: null,
				Fest: "重庆",
				dtime: "2018-11-01 07:04:00",
				paras: "0",
				aflightno: "8L9668",
				dflightno: "8L9503",
				IsVip: false,
				ParkingGate: "7",
				resulttype: null
			}
        ],

       nextNums:[
       {
				mdl: "B737",
				planeno: "B5231",
				Forg: "昆明",
				nation: "1",
				atime: "2018-10-31 19:08:00",
				business: "0",
				result: null,
				Fest: "昆明",
				dtime: "2018-11-01 07:56:00",
				paras: "0",
				aflightno: "MU5925",
				dflightno: "MU5735",
				IsVip: false,
				ParkingGate: "2",
				resulttype: null
			}, {
				mdl: "B737",
				planeno: "B5255",
				Forg: "重庆",
				nation: "1",
				atime: "2018-10-31 19:50:00",
				business: "0",
				result: null,
				Fest: "重庆",
				dtime: "2018-11-01 07:39:00",
				paras: "0",
				IsVip: false,
				ParkingGate: "1",
				resulttype: null
			}, {
				mdl: "A319",
				planeno: "B6210",
				Forg: "南宁",
				nation: "1",
				atime: "2018-10-31 23:02:00",
				business: "0",
				result: null,
			  Fest: "贵阳",
				dtime: "2018-11-01 07:22:00",
				paras: "0",
				aflightno: "JD5750",
				dflightno: "JD5637",
				IsVip: false,
				ParkingGate: "12",
				resulttype: null
			}, {
				mdl: "A320",
				planeno: "B1621",
				Forg: "石家庄",
				nation: "1",
				atime: "2018-10-31 23:47:00",
				business: "0",
				result: null,
				Fest: "长沙",
				dtime: "2018-11-01 07:49:00",
				paras: "0",
				aflightno: "JD5658",
				dflightno: "JD5189",
				IsVip: false,
				ParkingGate: "14",
				resulttype: null
			}, {
				mdl: "A320",
				planeno: "B6867",
				Forg: "浦东",
				nation: "1",
				atime: "2018-10-31 23:58:00",
				business: "0",
				result: null,
				Fest: "合肥",
				dtime: "2018-11-01 08:29:00",
				paras: "0",
				aflightno: "JD5666",
				dflightno: "JD5245",
				IsVip: false,
				ParkingGate: "10",
				resulttype: null
			}, {
				mdl: "B737",
				planeno: "B5292",
				Forg: "绵阳",
				nation: "1",
				atime: "2018-11-01 00:06:00",
				business: "0",
				result: null,
				Fest: "重庆",
				dtime: "2018-11-01 07:04:00",
				paras: "0",
				aflightno: "8L9668",
				dflightno: "8L9503",
				IsVip: false,
				ParkingGate: "7",
				resulttype: null
			}
        ],
        
            
     
        beAbandoned:[],
        

    }     
    },
    methods: {
      test:function(){
      // axios.request({
      //   method:"get",
      //   url:"http://47.92.202.234:8008/latest_data/"
      // })

      },

      sureSpeed:function(){
        console.log("ddd")
     
        window.clearInterval(this.setInterval1)
        // this.setIntervals.splice(0,1)
        // this.speed=parseFloat(this.speedInput)
        // // clearInterval
        this.setInterval1=setInterval(() => {
            this.scroll()
        }, parseFloat(this.selectList[this.optionValue-1] )*1000);
        // this.setIntervals.push(myInterval)

      },


     scroll:function () {
         this.remove();
         this.add()
         
     },   
    randomIndex: function () {
      return Math.floor(Math.random() * this.items.length)
    },
    add: function () {
    this.items.push(this.nextNums[0])
    this.nextNums.splice(0, 1)
    if(this.nextNums.length==0){
        this.nextNums=this.beAbandoned
        this.beAbandoned=[]

    }
    },
    remove: function () {
      this.beAbandoned.push(this.items[0])
      this.items.splice(0, 1)
      
    },
    shuffle: function () {
      this.items = _.shuffle(this.items)
    }
  },
  mounted:function(){
 
  },
  created:function(){
    //  this.setInterval1=setInterval(() => {
    //    this.scroll()
       
    //   }, 1500);
      

 
  },
  // 发送axios请求初始化数据

}
</script>

<style>

.list-complete-item {
/* 这里控制数据排放的方向 */
  transition: all 2s;
  display: block;
  margin-right: 30px;
}
.list-complete-enter, .list-complete-leave-to
/* .list-complete-leave-active for below version 2.1.8 */ {
  opacity: 0;
  /* 这里控制进入离开的方向 */
  transform: translateX(120px);
}
.list-complete-leave-active {
  position: absolute;
}

.tablediv{

    /* width:590px; */
    /* height: 350px; */
    /* margin-left:5%; 
    margin-right: 5%; */
   margin-top: 0px;
   margin-bottom: 0px
   
    

}

/* .flip-list-move {
  transition: transform 1s;
} */

</style>
