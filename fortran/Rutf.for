c  ********************************************************************
c     The subroutine lsfmin finds the minimum along the curve xi+s(xmu)
c     using only function evaluations
c----------------------------------------------------------------------
c ---------------------------------------------------------------------
      subroutine lsfmin(fu,n,x0,bl,bu,qt,d,e,wp,x,
     *                  f,x1,qs,y,wa,step0,cotmu,nmax,ierz,
     *                  ibound,jbound,nf1)
c-----------------------------------------------------------------------
c
c                       Arguments
c                       ---------
c     Input:
c
c        fu:  external function (see description in the main routine).
c         n:  number of variables.
c
c        x0:  starting point, n dimensional vector.
c        bl:  vector of lower bounds for constrained problems.
c        bu:  vector of upper bounds for constrained problems.
c        qt:  orthogonal factor of the Householder transformation.
c             corresponding to the Hessian matrix of the quadratic
c             model at x0.
c         d:  diagonal of the tridiagonal factor.
c         e:  subdiagonal of the tridiagonal factor.
c        wp:  - q * grad(x0).
c         x:  parameter of the subproblem g(x)= f(x0+ s(x)).
c         f:  f(x0).
c     step0:  initial estimation of the step lenght along the curve s(x).
c     cotmu:  upper bound for x.
c      nmax:  maximum allowable number of function evaluations.
c         y:  coordinates of the starting point in the original problem.
c        wa:  working vector.
c    ibound:  see definition in the main routine.
c    jbound:  see definition in the main routine.
c
c----------------------------------------------------------------------
c    Output:
c
c         x: best obtained point.
c        x1: new point, x1=x0+s(x).
c         f:  f(x1).
c        qs: q*(x1 - x0).
c         y: coordinates of x1 in the original problem.
c       nf1: number of function evaluations required by lsfmin.
c      ierz: error parameter
c            0 convergence has been achieved.
c            1 maximum number of function evaluations exceeded.
c            2 failure to converge.
c----------------------------------------------------------------------
      implicit real*8(a-h,o-z)
      dimension x0(n),wp(n),qt(n,n),d(n),e(n),x1(n),qs(n),
     *          y(n),wa(1),bl(n),bu(n),jbound(n)
      common/busca/anda,dnor,v1
      external fu
      data zero/0.d0/
c---------------------------------------------------------------------
      na1=1
      na2=na1+n
      na3=na2+n
      na4=na3+n
      nma1=na1-1
      nma2=na2-1
      nma3=na3-1
c----------------------------------------------------------------------
      nf1=1
      ierz=0
      nff=0
      eig=anda
c-----------------------------------------------------------------------
      vf0=f
      x00 = zero
      xb = zero
      fb = f

      do i=1,n
              wa(nma1+i)=x0(i)
              wa(nma2+i)=y(i)
              wa(nma3+i)=0.d0
      end do
c---------------------------------------------------------------------
c     Initialize parameter for the search.
c---------------------------------------------------------------------
      step=dmin1(cotmu*0.6d0,2.d0*step0)
      bound=cotmu
      xtol=step*0.25d0
      atol = dmax1(0.d0,xtol)
C---------------------------------------------------------------------
C     Calculate the next trial value of x.
C---------------------------------------------------------------------
      ifl = 1
 10   x = xb+step
      aux = xb+1.5d0*step

      if(dabs(aux-x00).ge.bound)then
              x = x00+dsign(bound,step)
              ifl = 2
      end if
C---------------------------------------------------------------------
C     Calculate the new value of f.
C---------------------------------------------------------------------
 20   if(nf1.ge.nmax)then
              ierz=1
              if(fb.ge.vf0)ierz=2
              go to 130
      else
              if(x.gt.zero)then
                      ax=v1/x - anda
                      call funct(fu,n,x0,bl,bu,d,e,qt,wp,ax,f,x1,y,qs,
     *	                     wa(na4),ibound,jbound,nff2)
                      nf1=nf1+1
              else
                      f=vf0
              end if
      end if
C---------------------------------------------------------------------
C     Reverse step if it seems to be uphill.
C---------------------------------------------------------------------
      if(nf1.gt.2)then
              if(f.ge.fb.and .fb.ge.vf0)then
                      bound=x
                      x00=zero
                      atol=x/3.d0
                      step=0.9d0*atol
                      ifl=3
                      xc=x
                      fc=f
                      go to 10
              else
                      go to 30
              end if
      else
c---------------------------------------------------------------------
c     Update the step.
c---------------------------------------------------------------------
              if(f.lt.fb)then
                      x00=x
                      bound=cotmu-x
                      if(eig.ge.1.d-5)then
                              step=step0-x
                              atol=0.7d0*step
                      else
                              if(eig.gt.0.d0)then
                                      step=dmin1(bound*0.6d0,9.d0*step0)
                                      atol=step/3.d0
                              else
                                      if(eig.le.0.d0)step=dmin1
     *		                       (bound*0.1d0,9.d0*step0)
                                      atol=step/3.d0
                              end if
                      end if
                      go to 40
              else
                      bound=x
                      x00=zero
                      atol=x/3.d0
                      step=0.9d0*atol
                      ifl=3
                      xc=x
                      fc=f
                      go to 10
              end if
      end if
 30   xd = xc
      fd = fc
      if(f.ge.fb)go to 50
c---------------------------------------------------------------------
c     Store in fb the best value of f (and the corresponding coordinates)
c     so far and rename the points previously computed.
C---------------------------------------------------------------------
 40   xc = xb
      fc = fb
      xb = x
      fb = f

      do i=1,n
              wa(nma1+i)=x1(i)
              wa(nma2+i)=y(i)
              wa(nma3+i)=qs(i)
      end do
C----------------------------------------------------------------------
c     Estimate the new displacement along the curve.
C----------------------------------------------------------------------
      if(ifl.ge.4) go to 60

      if(ifl.le.1)then
              if(nf1.gt.2)then
                      chx = (xb-xc)/(xb-xd)
                      chf = (fb-fc)/(fb-fd)
                      cs = 9.d0
                      if(chf.lt.chx)cs=1.5D0*(chx-chf/chx)/(chf-chx)
                      cs = dmin1(cs,9.d0)
                      cs = dmax1(cs,2.d0)
                      step = cs*step
              end if
              go to 10
      end if
C-----------------------------------------------------------------------
      if(ifl.ne.3)then
              ifl=3
              cs = dmax1(0.9d0*atol,0.01d0*dabs(xb-xc))
              x = xb+dsign(cs,xc-xb)
              if(dabs(x-xc).lt.dabs(x-xb)) x=0.5D0*(xb+xc)
              pend = (xb-x)/(xb-xc)
              if(pend.le.0.d0)go to 130
              go to 20
      else
c---------------------------------------------------------------------
c     Procedure when the point is close to 0 or cotmu.
c---------------------------------------------------------------------
              xa=xd
              fa=fd
              ifl=4
              go to 90
      end if
c---------------------------------------------------------------------
c     Return if the minimum seems to be outside the interval
c                         [0,cotmu]
c---------------------------------------------------------------------
 50   if(ifl.lt.4)then
              if(ifl.eq.3)go to 130
              xa=x
              fa=f
              ifl=4
              go to 90
      end if
c---------------------------------------------------------------------
c     Check the order of xa, xb, xc, xd.
c---------------------------------------------------------------------
      xc=x
      fc=f
 60   pend = (xb-xc)/(xa-xd)
      if(pend.gt.0.d0) go to 80
 70   h=xa
      xa=xd
      xd=h
      h=fa
      fa=fd
      fd=h
c---------------------------------------------------------------------
c     Set xb as the midpoint when three consecutive iterates
c     have the same functional value.
c---------------------------------------------------------------------
80    if(dabs(fa-fb).gt.zero)then
              if(dabs(fd-fb).le.zero.and.dabs(fc-fb).le.zero)then
                      xc=xb
                      xb=x
                      fc=fb
                      fb=f
                      go to 70
              end if
      end if
c-----------------------------------------------------------------------
c     Recompute the tolerance for accepting the optimum.
c-----------------------------------------------------------------------
90    da=(fb-fa)/(xb-xa)
      db=(fc-fb)/(xc-xb)
      if(ifl.lt.5)then
              ifl=5
              tol=0.01d0*dabs(xa-xc)
              tol=dmax1(tol,0.9d0*atol)
      else
              dc=(fd-fc)/(xd-xc)
              tol=0.d0
              if(dabs(db).gt.0.d0)then
                      tol=dabs(xa-xc)
                      pend=(dc-db)/(xa-xc)

                      if(pend.lt.0.d0)then
                              ct=0.5d0*dabs(db*((xd-xb)/(dc-db)+
     *		         (xa-xc)/(db-da)))
                              if(ct.lt.tol)tol=ct
                      end if
              end if
              tol=dmax1(tol,0.9d0*atol)
      end if
c---------------------------------------------------------------------
C     Set x to the minimizer of the interpolating quadratic.
c---------------------------------------------------------------------
      x=xb
      if(dabs(da-db).gt.0.d0)x=0.5d0*(da*(xb+xc)-db*(xa+xb))/(da-db)
c---------------------------------------------------------------------
c     Ensure that /xa-xb/.ge./xb-xc/.
c---------------------------------------------------------------------
      pend=(xa-xb)/(xb-xc)

      if(pend.lt.1.d0)then
              h=xa
              xa=xc
              xc=h
              h=fa
              fa=fc
              fc=h
      end if
c---------------------------------------------------------------------
c     Test convergence.
c---------------------------------------------------------------------
      if(dabs(xa-xb).le.atol)then
              if(fb.ge.vf0)then
                      ierz=1
              else
                      ierz=0
              end if
              go to 130
      end if
c---------------------------------------------------------------------
c     Choose the next x to save one function evaluation.
c---------------------------------------------------------------------
      pend=(xa-xb)/(xb-xc)

      if(pend.le.1.d1)then
              if(dabs(xa-xb).le.2.9D0*atol)then
                      x=0.5d0*(xa+xb)
                      if(dabs(x-xb).gt.atol)then
                              x=0.67d0*xb+0.33d0*xa
                      end if
c---------------------------------------------------------------------
c   Make sure that /x - xb/ < tol
c---------------------------------------------------------------------
              else
                      if(dabs(x-xb).lt.tol)then
                              x=xb+dsign(tol,x-xb)
                      else
                              go to 100
                      end if

                      if(dabs(x-xc).lt.dabs(x-xb))x=xb+dsign(tol,xa-xb)
                      if(dabs(x-xa).lt.dabs(x-xb))x=0.5d0*(xa+xb)
              end if
      else
c---------------------------------------------------------------------
c     Ensure that x is in the longer interval.
c---------------------------------------------------------------------
              cs=(x-xb)*dsign(3.d0,xa-xb)
              cs=dmax1(cs,tol,dabs(xb-xc))
              cs=dmin1(cs,0.1d0*dabs(xa-xb))
              x=xb+dsign(cs,xa-xb)
      end if
c---------------------------------------------------------------------
c     Test the possible effects of rounding errors.
c---------------------------------------------------------------------
 100  if(dabs(x-xb).gt.0.d0) then
              if((xa-x)/(xa-xb).le. 0.d0)go to 110
              if((x-xc)/(xa-xb).gt.0.d0) go to 20
      end if
c---------------------------------------------------------------------
C     Compute a new value of x in [xa,xb], if rounding errors allow
c     to find one.
c---------------------------------------------------------------------
 110  x=xa
 120  xx=0.5D0*(x+xb)
      pend=(xx-xb)/(xa-xb)

      if(pend.gt.0.d0)then
              pend=(x-xx)/(xa-xb)
              if(pend.gt.0.d0)then
                      x=xx
                      go to 120
              end if
      end if

      if(dabs(x-xa).gt.zero)go to 20
c---------------------------------------------------------------------
c     Return.
c---------------------------------------------------------------------
 130  x=xb
      f=fb

      do i=1,n
              x1(i)=wa(nma1+i)
              y(i)=wa(nma2+i)
              qs(i)= wa(nma3+i)
      end do

      nf1=nf1-1
      return
      end
c  ********************************************************************
c----------------------------------------------------------------------
      subroutine numhes(n,x,f,h,fu,del,fp,fm,nfu)
      implicit real*8(a-h,o-z)
      dimension x(n),h(1),del(n),fp(n),fm(n)
      external fu
c----------------------------------------------------------------------
c  --------------------------------------------------------------------
c                       Arguments
c                       ---------
c
c         n:  dimension of x.
c
c         x:  n-dimensional vector (current point).
c
c         f:  value of the function at the point x.
c
c         h:  the lower triangular portion of the numerically
c             estimated hessian (output).
c
c        fu:  user supplied subroutine which computes the function
c             to be minimized.
c
c       del:  n dimensional vectors containing the increments given
c             by the subroutine hesdel.
c
c     fp,fm:  working vectors.
c
c       nfu:  number of function evaluations.
c
c----------------------------------------------------------------------
      nf0=nfu
      do j=1,n
	  call hesdel(x(j),hj,f)
              if(x(j).lt.0.d0)hj=-hj
              del(j)=hj
	  xj=x(j)
	  x(j)=x(j)+hj
	  call fu(n,x,fp(j))
              nfu=nfu+1
              x(j)=xj
              x(j)=x(j)-hj
	  call fu(n,x,fm(j))
              nfu=nfu+1
              x(j)=xj
      end do
      k=0
      do i=1,n
              xi=x(i)
              x(i)=x(i)+del(i)
              do j=1,i-1
                      xj=x(j)
                      x(j)=x(j)+del(j)
	          call fu(n,x,fij)
                      nfu=nfu+1
	          x(j)=xj
                      h(k+j)=(fij-fp(j)-fp(i)+f)/(del(i)*del(j))
              end do
              k=k+i
              h(k)=(fp(i)-2.d0*f+fm(i))/(del(i))**2
              x(i)=xi
      end do
      return
      end
c--------------------------------------------------------------------
c**********************************************************************
c----------------------------------------------------------------------
      subroutine hesdel(x,del,f)
      implicit real*8(a-h,o-z)
      dimension alfa(4)
c----------------------------------------------------------------------
c  --------------------------------------------------------------------
c                       Arguments
c
c     Input:
c
c         x:  n-dimensional vector (current point).
c
c         f:  value of the function at the point x.
c
c----------------------------------------------------------------------
c    Output:
c
c       del:  increment for estimating the hessian, computed by means
c             of a new algorithm which generalizes the standard one
c             described e.g.in the book:
c             J.E.Dennis Jr. and R.B.Schnabel," Numerical Methods
c             for Unconstrained Optimization and Nonlinear Equations",
c             Prentice Hall,1983".
c             This value is used by the routine numhes.
c
c----------------------------------------------------------------------
      data tol/0.10842021724855d-18/,crtol/.47683715820312D-06/
      data alfa/.3669535090D+00,.3750461917D-02,
     *         -.5118486647D-01,.5788890042D-02/
c------------------------------------------------------------------------
      c=dabs(f)
      id=0
      if(c.gt.0.d0) then
	id=dlog10(c)
	if(id.gt.0)id=id+1
      end if
      c=dabs(x)
      ib=0
      if(c.gt.0.d0) then
	ib=dlog10(c)
	if(ib.eq.0)ib=ib+1
      end if
      if(id.gt.0)then
	del=alfa(1)**ib*alfa(2)**id*alfa(3)+alfa(4)*c
      else
	del=crtol*dmax1(0.1d0,c)
      end if
      if(dabs(del).lt.tol*c)then
	s=1.d0
	if(del.lt.0.d0)s=-s
	del=s*crtol*dmax1(0.1d0,c)
      end if
      return
      end
c  ********************************************************************
c----------------------------------------------------------------------
c   Function ierstf checks convergence. In constrained problems
c   if necessary, it changes the current iterate, in order to
c   avoid stationary points of the auxiliary problem.
c----------------------------------------------------------------------
      integer function ierstf(n,bl,bu,x,f,gx,gz,z,eps,nfu,
     * gp,fu,idiff,ibound,jbound)
c----------------------------------------------------------------------
c                       Arguments
c                       ---------
c    Input :
c
c        n :  number of variables.
c       bl :  vector of lower bounds.
c       bu :  vector of upper bounds.
c        x :  current iterate of the unconstrained problem.
c        f :  f(x).
c       gx :  gradient at x.
c        z :  coordinates of the point x in the constrained problem.
c       gz :  gradient at z.
c      eps :  tolerance for the optimality test.
c      nfu :  number of function evaluations.
c       fu :  external function (see main routine).
c    idiff :  see definition in the main routine.
c   ibound :  see definition in the main routine.
c   jbound :  see definition in the main routine.
c
c   Output :
c
c        x :  current iterate or a modification of it.
c        f :  f(x).
c       gx :  gradient at x.
c        z :  coordinates of x in the constrained problem.
c       gz :  gradient at z .
c       gp :  projection of gz onto the domain of the original problem.
c      nfu :  number of function evaluations.
c
c----------------------------------------------------------------------
      implicit real*8(a-h,o-z)
      dimension x(n),z(n),gx(n),bl(n),bu(n),gz(n),gp(n),jbound(n)
      common/npar/maxfun
      common/ierp/ierp
      external fu

      ierstf=-1
c----------------------------------------------------------------------
c     Optimality test
c----------------------------------------------------------------------
10    smax=0.d0
      smgx=dnrm2(n,gx,1)
      s1=dmax1(dabs(f),1.d0)

      do i=1,n
              s2=dmax1(dabs(x(i)),1.d0)
              s3= dabs(gx(i))*s2/s1
              if(s3.gt.smax)smax= s3
      end do
c----------------------------------------------------------------------
c     Optimality test for ibound=0
c----------------------------------------------------------------------
      if(ibound.eq.0)then
	  if(smax.le.eps.or.(ierp.eq.2.and.smgx.lt.5.d0*eps))then
                      smax=smgx
                      ierstf=0
                      return
              else
                      go to 20
              end if
      else
c----------------------------------------------------------------------
c     The projection of gz onto the domain of the original problem
c     is calculated, and the optimality test is performed. If
c     satisfied, return.
c----------------------------------------------------------------------
      do i=1,n
              gp(i)=gz(i)

              if(jbound(i).eq.1.or.jbound(i).eq.3)then
                      bcot=dmax1(1.d-5,dabs(bu(i))* 1.d-8)
                      if(dabs(z(i)-bu(i)).le.bcot.and.gz(i).lt.0.d0)
     *	          gp(i)=0.d0
              end if

              if(jbound(i).gt.1)then
                      bcoi=dmax1(1.d-5,dabs(bl(i))*1.d-8)
                      if(dabs(z(i)-bl(i)).le.bcoi.and.gz(i).gt.0.d0)
     *	          gp(i)=0.d0
              end if

      end do

      smaz=0.d0
      smgp=dnrm2(n,gp,1)
      smgx=dnrm2(n,gx,1)

      do i=1,n
              sz=dmax1(dabs(z(i)),1.d0)
              si= dabs(gp(i))*sz/s1
              if(si.gt.smaz)smaz= si
      end do

      if(smaz.le.eps.or.smgp.le.eps)then
              ierstf=0
              return
      else
              if(ierp.eq.2 .and.(smaz.le.5.d0*eps.or.smgp.le.5.d0*eps))
     *        then
                      ierstf=0
                      return
              end if
      end if

      if(dmin1(smgx,smax).le.eps)then
              if(dmin1(smgx,smax).gt.1.d-2*eps.and.
     *        dmin1(smaz,smgp).lt.1.d2*eps) go to 20
c----------------------------------------------------------------------
c     If the norm of the gradient at x is too small when
c     compared with the one of the projected gradient gp at z,
c     the current iterate is perturbed.
c     z, x, f, gz, gx at the perturbed point are computed.
c----------------------------------------------------------------------
      if(dmin1(smgx,smax).lt.1.d-4*dmin1(smaz,smgp))then
              ierstf=-2
              call transf2(n,bl,bu,gp,z,x,f,fu,jbound,nfu)
              call nugrad(n,z,fu,f,gz,1,idiff,nfu)
              call gradx(n,x,bl,bu,gz,gx,jbound)
c----------------------------------------------------------------------
c     Analize if the optimality criterion is satisfied.
c----------------------------------------------------------------------
              go to 10
      end if
      end if
      end if
c----------------------------------------------------------------------
c     Return if the maximum number of
c     function evaluations is exceeded.
c----------------------------------------------------------------------
20    if(nfu.ge.maxfun)then
              ierstf=1
      end if

      return
      end
c**********************************************************************

c----------------------------------------------------------------------

c----------------------------------------------------------------------

      subroutine nugrad(n,x,fu,fx,g,ifx,idiff,nfu)
c
c ---------------------------------------------------------------------
c  Purpose: to compute a numerical approximation to the gradient
c  of the function defined in the subroutine fu using a new
c  algorithm.
c ----------------------------------------------------------------
c                       Arguments
c                       ---------
c
c     Input :
c         n : number of variables
c         x : n dimensional vector (current point)
c        fu : subroutine of the form - subroutine fu(n,x,fx)
c        fx : fu(x) (see the parameter ifx)  !Ale: f en nugrad
c       ifx : if equal to 1 it is assumed that fx=fu(x)
c             otherwise fx=fu(x) is computed
c     idiff : if equal to 1 forward differences are used
c             if equal to 2 central differences are used
c
c    Output :
c         g : output containing the numerical gradient
c
c                      Author: Hugo D.Scolnik
c                Last revision: December 12th,1994
c ----------------------------------------------------------------

      implicit real*8(a-h,o-z)
      dimension x(1),g(1)
C --  No sé bien para qué usa ls
      common/lsearch/ls
C -- ALFAs (para central differences)--
      DATA alfa1/19.9879581887312838d0/,
     *     alfa2/3.11786317285359073d0/,
     *     alfa3/0.107810877267449908d-11/,
     *     alfa4/0.689956d-5/,

C -- BETAs (para central differences)--
     *     beta1/53.1036811792759202d0/,
     *     beta2/2.36701536161196047d0/,
     *     beta3/0.66580545056039918d-12/,
     *     beta4/1.d-7/,

C Usado para definir delta en ambas differences cuando es id <= -1 (se multiplica con un max de 2 cosas)
     *     dqtol/0.32927225399136d-9/

C --  No sé bien para qué usa ls
C     *     ls=4
C Si no me pasan el valor de fu(x) entonces calcularlo
      if(ifx.eq.0)then
C Llamar a fu con x y sumar uno al contador de llamadas
      call fu(n,x,fx)
      nfu=nfu+1
      end if
C ----- APLICAR SUB-HEURÍSTICA 1 sobre fu(x) -----
C Buscar el valor absoluto de fu(x) y si es 0 ir a 20
      c=dabs(fx)
      if(c.eq.0.d0)go to 20
C Si fu(x) != 0, buscarle su log en base 10 y guardarlo en id
      id=dlog10(c)
C Si log_10(fu(x)) > 0 entonces sumar 1 a id (donde había guardado al log)
      if(id.gt.0)id=id+1
      go to 30
C Asignarle 0 a id, que arriba puede ser o "log_10(fu(x))" o eso + 1
20    id=0
C ----- FIN SUB-HEURÍSTICA 1 sobre fu(x) -----
C Iterar las posiciones de x haciendo operaciones sobre ellas de forma aislada (creo, antes de haber leer todo bien)
30    do 70 i=1,n
C ----- APLICAR SUB-HEURÍSTICA 1 sobre x(i) ----- (la misma que con fu(x) al principio)
              a=dabs(x(i))
              if(a.eq.0.d0)go to 40
              ib=dlog10(a)
              if(ib.eq.0)ib=ib+1
              go to 50
40            ib=0
C ----- FIN SUB-HEURÍSTICA 1 sobre x(i) -----
C Ver si aplicar forward (idiff = 1) or central differences (idiff = 2)
50            if(idiff.eq.2)go to 60
C -- Aplicar forward differences (usa los beta)--
C Si id (heuŕistica sobre fu(x)) > -1
              if(id.gt.-1)then
C Fórmula rara con los beta1 a beta4 (a simple vista no la entiendo)
                      ae=beta1**ib*beta2**id*beta3
                      delta=ae+beta4*a
              else
C Creo que acá define a delta usando un "mínimo valor posible" de id
                      delta=dqtol*dmax1(0.1d0,a)
              end if
C Aplicar resultados de las heurísticas de betas sobre x(i) y llamar a f(x) y guardar el resultado de este "mini-movimiento unidemsional" sobre fr
      b=x(i)
      x(i)=b+delta
      call fu(n,x,fr)
      nfu=nfu+1
C Volver a x(i) a su valor anterior (antes de apicarle los resultados de las heurísticas)
      x(i)=b
C Calcular en g(i) la diferencia entre el fu(x) original y el fu(x') con x(i) cambiado
      g(i)=(fr-fx)/delta
      go to 70
60    continue
C -- Aplicar central differences (usa los alfa)--
      if(id.gt.-1)then
C Fórmula rara con los alfa1 a alfa4 (a simple vista no la entiendo)
            ae=alfa1**ib*alfa2**id*alfa3
            delta=ae+alfa4*a
      else
C Creo que acá define a delta usando un "mínimo valor posible" de id
            delta=dqtol*dmax1(0.1d0,a)
      end if
C Aplicar resultados de las heurísticas de alfas sobre x(i) y llamar a f(x) y guardar el resultado de este "mini-movimiento unidemsional" sobre fr
      b=x(i)
      x(i)=b+delta
      call fu(n,x,fr)
      nfu=nfu+1
      x(i)=b-delta
      call fu(n,x,fl)
      nfu=nfu+1
      x(i)=b
C Calcular en g(i) la diferencia entre el fu(x) original y el fu(x') con x(i) cambiado
      g(i)=0.5d0*(fr-fl)/delta
70    continue
      return
      end
c  ********************************************************************
c----------------------------------------------------------------------
c     This subroutine computes the sparse secant update  Tk+1,
c     using the least-change theory.
c----------------------------------------------------------------------
      subroutine updaf(n,bl,bu,d,e,qt,sq,xk,fu,ng,gk,gkp1,
     *                  wa,ibound,jbound,nfu,idiff)
c----------------------------------------------------------------------
c                       Arguments
c                       ---------
c     Input:
c
c        n :  dimension of the problem.
c       bl :  vector of lower bounds.
c       bu :  vector of upper bounds.
c        d :  diagonal of the tridiagonal matrix Tk.
c        e :  subdiagonal of the tridiagonal matrix Tk.
c       qt :  orthogonal matrix of the factorization Qt*Tk*Q at xk.
c       sq :  vector Q*s where, s= xc-xk, xc is the current iterate.
c       xk :  previous iterate.
c        fu:  user supplied function.
c       gk :  gradient at xk.
c     gkp1 :  gradient at xk+s.
c       wa :  working vector.
c    ibound:  see definition in the main routine.
c    jbound:  see definition in the main routine.
c       nfu:  number of function evaluations.
c     idiff:  see definition in the main routine.
c    Output:
c
c         d:   diagonal of the updated matrix Tk+1
c         e:   subdiagonal of the matrix Tk+1
c        ng:   number of gradient evaluations needed for ensuring
c              the 'bounded norm condition' of Tk
c              (see the reference).
c----------------------------------------------------------------------
      implicit real*8 (a-h,o-z)
      dimension d(n),e(n),qt(n,n),sq(n),xk(n),gk(n),gkp1(n),wa(1),
     *          bl(n),bu(n),jbound(n)
      external fu
      data tol/0.10842022d-18/
      np1=0
      np2=np1+n
      nyq=np2+n
      nwt=nyq+n
      nwt2=nyq
      nwt1=nwt+1
      nwt21=nwt2+1
      nwt3=nwt+n
      nwt31=nwt3+1
      nwty=nwt3+n
      nwty1=nwty+1
      nwgy=nwty+n
      nwgy1=nwgy+1
      ng=0
      nm1=n-1
      xr=dnrm2(n,sq,1)
      sts=xr*xr
      axr=tol*xr

      do j=1,n
              wa(nwt3+j)=gkp1(j)
      end do

      ma=1
c----------------------------------------------------------------------
c     Analize if the condition sq(i+1)**2+sq(i)**2 > 0 holds.
c----------------------------------------------------------------------
      do while (ma.eq.1)
              ma=0
              i=2
              s1=sq(1)*sq(1)
              si=s1
              do while (i.le.n.and.ma.eq.0)
                      sii=si
                      si=sq(i)*sq(i)

                      if(dsqrt(sii+si).ge.axr)then
                              i=i+1
                      else
                              ma=1
                      end if
              end do

              if(dsqrt(s1+si).lt.axr) ma=1
c----------------------------------------------------------------------
c     If necessary, modify the step sq and in such a case
c     calculate the gradient at xk+Qt*sq
c----------------------------------------------------------------------
      if (ma.eq.1) then
              drn=dsqrt(dfloat(n))
              do ik=1,n
                     sq(ik)=xr/drn
              end do
              call matmul(n,qt,sq,1,wa(nwt21))

              do kl=1,n
                     wa(nwt+kl)=xk(kl)+wa(nwt2+kl)
              end do
              if(ibound.eq.0)then
                     call nugrad(n,wa(nwt1),fu,f,wa(nwt31),0,idiff,nfu)
              else
                     call transf(n,1,wa(nwty1),bl,bu,2,wa(nwt1),jbound
     *	          ,ir)
                     call nugrad(n,wa(nwty1),fu,f,wa(nwgy1),0,idiff,nfu)
                     call gradx(n,wa(nwt1),bl,bu,wa(nwgy1),wa(nwt31),
     *	         jbound)
              end if
      end if
      end do
c----------------------------------------------------------------------
c     Restore qy=Q*(grad(xk+Qt*sq)-gk)
c----------------------------------------------------------------------
      do j=1,n
              wa(nwt+j)=wa(nwt3+j)-gk(j)
      end do

      call matmul(n,qt,wa(nwt1),2,wa(nyq+1))
c----------------------------------------------------------------------
c     Compute the elements of the matrix P and set the
c     parameters for Tri1
c----------------------------------------------------------------------
      wa(np1+1)=0.d0
      a2=s1/sts
      wa(np2+1)=2.d0*a2
      wa(nyq+1)=wa(nyq+1)-d(1)*sq(1)

      if(n.ge. 2)then
              a3=sq(2)*sq(2)/sts
              wa(np2+1)=wa(np2+1)+a3
              wa(nyq+1)=wa(nyq+1)-e(2)*sq(2)

              if(n.gt.2)then
                      do i=2,nm1
                              a1=a2
                              a2=a3
                              a3=sq(i+1)**2 /sts
                              wa(np1+i)=sq(i)*sq(i-1)/sts
                              wa(np2+i)=a1+2.d0*a2+a3
                              wa(nyq+i)=wa(nyq+i)-e(i)*sq(i-1)-e(i+1)*
     *		      sq(i+1)-d(i)*sq(i)
                      end do
              end if

              wa(np1+n)=sq(n)*sq(n-1)/sts
              wa(np2+n)=a2+2.d0*a3
              wa(nyq+n)=wa(nyq+n)-e(n)*sq(n-1)-d(n)*sq(n)
              do i=2,n
                      wa(np1+i-1)=wa(np1+i)
              end do
              wa(np1+n)=0.d0
      end if
c----------------------------------------------------------------------
c     Solve the tridiagonal system P*v= qy - Tk*sq
c----------------------------------------------------------------------
      call tri1(n,wa(np2+1),wa(np1+1),wa(nyq+1))
c----------------------------------------------------------------------
c     Find the diagonal and subdiagonal of Tk+1
c     using Tk+1 = Tk+ Proj( sq* vt + v* sqt), where
c     Proj is the orthogonal projector onto the subspace
c     of the symmetric tridiagonal matrices.
c----------------------------------------------------------------------
      d(1)=d(1)+2.0d0*wa(nyq+1)*sq(1)/sts

      if(n.ge.2)then

              do i=2,n
                      d(i)=d(i)+2.d0*wa(nyq+i)*sq(i)/sts
                      e(i)=e(i)+(wa(nyq+i)*sq(i-1)+wa(nyq+i-1)*sq(i))/
     *	          sts
              end do
      end if

      return
      end

