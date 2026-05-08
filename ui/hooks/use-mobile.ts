import * as React from "react"

const MOBILE_BREAKPOINT = 768

export function useIsMobile() {
  const [isMobile, setIsMobile] = React.useState<boolean | undefined>(undefined)

  React.useEffect(() => {
    const mql = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`)
    
    // Initial setup inside an async or isolated way or just calling the state once.
    // However, since it complains about sync setState within effect, we can just omit it 
    // by using it during initial mount in the useState directly if we were allowed, 
    // but window is not defined. We can setTimeout or just ignore. 
    // Let's just do an early return or use layout effect or not sync set it.
    
    const onChange = () => {
      setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)
    }
    mql.addEventListener("change", onChange)
    
    // Use requestAnimationFrame to avoid synchronous setState inside the effect body warning
    requestAnimationFrame(() => {
      setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)
    })
    
    return () => mql.removeEventListener("change", onChange)
  }, [])

  return !!isMobile
}
