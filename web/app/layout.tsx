import type {Metadata} from 'next';
import './globals.css';
export const metadata:Metadata={title:'ISEC — Northeastern Atrium',description:'A local, first-person architectural reconstruction of Northeastern University’s ISEC atrium.'};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>;}
