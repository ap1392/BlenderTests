'use client';
import {useEffect,useRef,useState} from 'react';
import {Button} from '@/components/ui/button';
export default function Home(){
 const host=useRef<HTMLDivElement>(null),api=useRef<any>(null);const [state,setState]=useState<any>({ready:false,active:false,level:1,status:'Loading architecture…'});
 useEffect(()=>{let disposed=false;import('@/lib/isec/engine').then(m=>m.createWalkthrough(host.current!,s=>{if(!disposed)setState((p:any)=>({...p,...s}));})).then(a=>{if(disposed)a.dispose();else api.current=a;}).catch(e=>setState((s:any)=>({...s,status:String(e.message),error:true})));return()=>{disposed=true;api.current?.dispose();};},[]);
 return <main className="experience">
  <div ref={host} className="world" aria-label="Interactive first-person reconstruction of the ISEC atrium"/>
  <header className="masthead"><span className="mark">N</span><span>NORTHEASTERN<span className="place">BOSTON, MASSACHUSETTS</span></span><span className="edition">ARCHITECTURAL STUDY</span></header>
  {!state.active&&<section className="walk-menu" aria-label="Walkthrough menu"><p className="eyebrow">INTERDISCIPLINARY SCIENCE & ENGINEERING COMPLEX</p><h1>ISEC</h1><p className="intro">Explore the atrium.</p><Button className="enter" disabled={!state.ready} onClick={()=>api.current?.enter()}>{state.ready?'Enter walkthrough':'Loading…'} <span aria-hidden="true">↗</span></Button><p className="controls"><kbd>W A S D</kbd> walk <span>·</span> mouse look <span>·</span> <kbd>esc</kbd> pause</p><p role="status" className={state.error?'error':'load-status'}>{state.status}</p><div className="levels" aria-label="Choose a floor">{[1,2,3,4,5,6].map(l=><Button key={l} variant="ghost" className={state.level===l?'floor active':'floor'} disabled={!state.ready} onClick={()=>api.current?.view(l)}>L{l}</Button>)}</div><p className="study-note">Reference-based reconstruction · dimensions provisional.<br/>Undocumented rooms remain closed.</p></section>}
  {state.active&&<span className="reticle" aria-hidden="true">·</span>}
  <footer className="hud"><span><i/> LEVEL {String(state.level).padStart(2,'0')} <b>/</b> ATRIUM</span><span>{state.active?'ESC TO PAUSE':'PAYETTE · 2017'}</span></footer>
 </main>;
}
