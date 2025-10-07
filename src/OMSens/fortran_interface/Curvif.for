c ********************************************************************
c     This is the file curvif.for using only function values
c     El paquete completo incluye los archivos CURVIf (éste), CURVIg, y CURVIh según se tengan solamente valores de la función, 
c     o además gradientes y hessianos respectivamente
c ---------------------------------------------------------------------
      subroutine curvif(fu, n, x0, fopt, eps, ibound,
     *                  jbound, bl, bu, wa, nfu, nit, idiff, kmax, ier)
C     !ms$attributes DLLEXPORT :: curvif
c
c  --------------------------------------------------------------------
c                       Arguments
c                       ---------
c     Input:
c
c        fu:  user supplied subroutine which computes the function
c             to be minimized.
c
c     Usage:  call fu(n,x,f)
c         n:  dimension of x.
c         x:  n-dimensional vector.
c         f:  value of the function at the point x.    ! Ale: fx en nugrad
c
c         n:  dimension of the problem.
c
c        x0:  initial guess point.
c
c       eps:  tolerance for the stopping criterion.
c
c    ibound:  parameter such that if equal to
c             0 is an unconstrained problem
c             1 is a constrained problem.
c
c    jbound:  working vector of dimension n defining the sort of
c             constraint for each variable (only used when ibound.ne.0).
c             jbound(i) = 0 if the ith variable has no constraints.
c                         1 if the ith variable has only upper bounds.
c                         2 if the ith variable has only lower bounds.
c                         3 if the ith variable has both upper and
c                           lower bounds.
c
c        bl:  vector of lower bounds (not used if ibound=0).
c
c        bu:  vector of upper bounds (not used if ibound=0).
c
c        wa:  working vector of dimension (see output)
c             9*n+n*(n+1)/2+n*n+max(7*n-n*(n+1)/2,0)
c
c       nfu:  maximum number of function evaluations. If equal to
c             zero, the default value of 5000*n is used.
c
c     idiff:  Choose forward or central differences. Forward
c             differences require fewer function evaluations and
c             should be favored unless the problem is exceedingly
c             difficult.
c             idiff = 1  forward differences
c             idiff = 2  central differences
c
c     kmax:   The parameter kmax is such that the hessian is
c             recomputed every kmax iterations.
c             We recommend kmax = 3 unless the problem is
c             very difficult.  In this case choose kmax = 1 or 2.
c----------------------------------------------------------------------
c    Output:
c
c        x0:  best obtained point.
c
c      fopt:  value of the function at the point x0.
c
c       nfu:  number of function evaluations.
c
c       nit:  number of iterations.
c
c        wa:  this vector contains gradient(x0) in the unconstrained
c             case, and the projected gradient(x0) for constrained
c             problems.
c
c       ier:  0 convergence has been achieved.
c             1 maximum number of function evaluations exceeded.
c             2 failure to converge.
c             3 wrong input in a constrained problem. In such a case
c               the components of vectors bl and bu set to 1.d30
c               were ill defined on input.
c----------------------------------------------------------------------
c      The algorithm for unconstrained optimization is described in:
c       "A curvilinear search using tridiagonal secant updates for
c                    unconstrained optimization"
c      J.E.Dennis,N.Echebest,M.T.Guardarucci,J.M.Martinez,H.D.Scolnik
c      and C.Vacchino.
c      SIAM J. on Optimization, Vol.1, Number 3, August 1991, page 351
c----------------------------------------------------------------------
c   WARRANTY  - BYTECH ARGENTINA warrants only that our own testing
c               procedures has been applied to this code.
c
c        No other warranty, expressed or implied is applicable.
c----------------------------------------------------------------------
c   Technical support: send mail to -->   hugo@nobi.uba.ar
c----------------------------------------------------------------------
c               Latest revision: January 2, 1996
c----------------------------------------------------------------------
      implicit real*8 (a-h,o-z)
      dimension x0(n),wa(1),bl(n),bu(n),jbound(n)
      common /busca/eig,dnor,v1
      common/npar/maxfun
      common/ierp/ierp
      external fu
c----------------------------------------------------------------------
c
c     The parameter kmax is such that the hessian is recomputed every
c     kmax iterations. For every other iteration only the tridiagonal
c     matrix T is updated in the decomposition H = Q(t)*T*Q using
c     the least change secant update theory (see reference).
c     Hence, larger values of kmax lead to fewer hessian evaluations.
c     The chosen value of 3 has been found experimentally to be a good
c     compromise between highly and mildly nonlinear problems.
c
c----------------------------------------------------------------------
c                data kmax/3/
      data sal/1.d-5/
      ier=0
      ierp=0
      n1=n*(n+1)/2
c----------------------------------------------------------------------
c     Set up pointers of the working vector.
c----------------------------------------------------------------------
c     Pointers for the working vector wa( ) are as follows:
c     nx1  :  the new point x1.
c     ngr0 :  the gradient at the point x0.
c     ngry :  ngr0+n
c     nxy  :  ngry+n
c     ngr1 :  the gradient at the new point.
c     nqt  :  Q transposed, where Q is an orthogonal matrix.
c     nhe  :  the Hessian
c     nd   :  diagonal  of the  tridiagonal matrix
c     ne   :  subdiagonal of the tridiagonal matrix
c     nw   :  - Q*grad0
c     nsq  :  Q*s
c----------------------------------------------------------------------
      nqt=1
      nx1=nqt+n*n
      ngr0=nx1+n
      ngry=ngr0+n
      nxy=ngry+n
      ngr1=nxy+n
      nw=ngr1+n
      nsq=nw+n
      nd=nsq+n
      ne=nd+n
      nhe=ne+n
      naux1=nhe
      naux2=nx1
c----------------------------------------------------------------------
c     Auxiliar indexes.
c----------------------------------------------------------------------
      nmx1=nx1-1
      nmgr0=ngr0-1
      nmgr1=ngr1-1
      nmgry=ngry-1
      nmxy=nxy-1
      nmw=nw-1
      nmqt=nqt-1
      nmd=nd-1
      nme=ne-1
      ndc=naux1-1
      nec=naux2-1
c---------------------------------------------------------------------
c     Set default value for maxfun
c----------------------------------------------------------------------
      maxfun=5000*n
      if(nfu.gt.0)maxfun=nfu
      nit=0
      nfu=0
c----------------------------------------------------------------------
c     Compute initial values of function and gradient.
c----------------------------------------------------------------------
      if(ibound.eq.0)then
              call fu(n,x0,fopt)
              nfu=nfu+1
              call nugrad(n,x0,fu,fopt,wa(ngr0),1,idiff,nfu)
      else
c ---------------------------------------------------------------------
c     If it is a constrained problem is transformed into an
c     unconstrained one according to ibound.
c     The initial point is stored in wa(nxy).
c----------------------------------------------------------------------
              do i=1,n
                      wa(nmxy+i)=x0(i)
              end do
c----------------------------------------------------------------------
c     x0, although transformed, is kept as the starting point of the
c     new unconstrained problem.
c----------------------------------------------------------------------
              call transf(n,nfu,wa(nxy),bl,bu,1,x0,jbound,ier)
              if(ier.eq.3)return
              call fu(n,wa(nxy),fopt)
              nfu=nfu+1
              call nugrad(n,wa(nxy),fu,fopt,wa(ngry),1,idiff,nfu)
              call gradx(n,x0,bl,bu,wa(ngry),wa(ngr0),jbound)
      end if
c----------------------------------------------------------------------
c     Optimality test.
c----------------------------------------------------------------------
      ier=ierstf(n,bl,bu,x0,fopt,wa(ngr0),wa(ngry),wa(nxy),eps,nfu,
     *          wa(naux1),fu,idiff,ibound,jbound)
      if (ier.gt.-1) go to 40
      kal=0
10    k=1
c----------------------------------------------------------------------
c     Compute and factorize the Hessian
c     as h=Qt*T*Q , where Q is an
c     orthogonal matrix and T is a
c     tridiagonal matrix.
c----------------------------------------------------------------------
      f=fopt
      if(ibound.eq.0)then
              call numhes(n,x0,f,wa(nhe),fu,wa(nx1),wa(ngr1),wa(nw),nfu)
      else
c----------------------------------------------------------------------
c     The Hessian of the constrained problem is stored in wa(nxy)
c     and the Hessian of the unconstrained one in x0
c----------------------------------------------------------------------
              call numhes(n,wa(nxy),f,wa(nhe),fu,wa(nx1),wa(ngr1),
     *                    wa(nw),nfu)
              call hessix(n,x0,bl,bu,wa(ngry),wa(nhe),jbound)
      end if
c----------------------------------------------------------------------
      call factor(n,n1,wa(nhe),wa(nqt),wa(nd),wa(ne),0)
20    nit=nit+1
c----------------------------------------------------------------------
c     Compute the smallest eigenvalue of
c     the tridiagonal matrix.
c     Set parameters for "lsfmin"  (line search without derivatives)
c----------------------------------------------------------------------
      do i=1,n
              wa(ndc+i)=wa(nmd+i)
              wa(nec+i)=wa(nme+i)**2
      end do

      call autova(wa(naux1),wa(naux2),n)
      eig=wa(naux1)
      dnor=dnrm2(n,wa(ngr0),1)
      v1=1.d0
      v3=sal

      if (eig.ge.sal) then
              cotmu=v1/eig
              step= cotmu
      else
              if(eig.gt.0.d0)then
                      v1=5.d0*eig
                      cotmu= v1/(eig)
                      step= v1/(eig+(sal-eig)+1.d-2*dsqrt(dnor))
              else
                      v2=1.d0
                      v1=1.d0
                      if(dnor.gt.1.d2) v2=1.d-1
                      cotmu=v1/sal
                      v3=dmax1(sal, 1.d-1*dabs(eig))
                      step=v1/(v3+v2*dsqrt(dnor))
              end if
      end if

      iqt=nmqt

      do j=1,n
              aw=0.d0
              do i=1,n
                      iqt=iqt+1
                      aw=aw-wa(iqt)*wa(nmgr0+i)
              end do
              wa(nmw+j)=aw
      end do
c-----------------------------------------------------------------------
c     Define parameters for lsfmin.
c-----------------------------------------------------------------------
      f=fopt
      step0=step
      xmu=0.d0
      dgg=dnor*dnor
      der=-dgg/v1
      maxfn=50
c---------------------------------------------------------------------
      call lsfmin(fu,n,x0,bl,bu,wa(nqt),wa(nd),wa(ne),wa(nw),xmu,
     * f,wa(nx1),wa(nsq),wa(nxy),wa(naux1),step0,cotmu,
     * maxfn,ierz,ibound,jbound,nf1)
c----------------------------------------------------------------------
c     Analize the amount of descent of the function and the step
c     s(xmu) from the curvilinear search.
c     Analize alternatives for improving the descent.
c     Analyze alternatives if lsfmin did not converge.
c----------------------------------------------------------------------
      nfu=nfu+nf1
      sder=0.d0
      sver=0.d0
      dx0=dnrm2(n,x0,1)

      do i=1,n
              sder=sder+wa(nmgr0+i)*(wa(nmx1+i)-x0(i))
              sver=dmax1(dabs(wa(nmx1+i)-x0(i)),sver)
      end do

      if(sver.le.1.d-13*dmax1(1.d0,dx0).or.ierz.gt.0)then
              k=kmax
              ierp=2
      end if

      if((f-fopt).le.0.9d0*der*xmu.or.(f-fopt).le.7.d-1*sder)then
              if(k.gt.3)then
                      k=kmax
              end if
      end if
c--------------------------------------------------------------------
c     Calculate the gradient at the new iterate x1
c--------------------------------------------------------------------
      f1=f
      if(ibound.eq.0)then
              call nugrad(n,wa(nx1),fu,f,wa(ngr1),1,idiff,nfu)
      else
              call nugrad(n,wa(nxy),fu,f,wa(ngry),1,idiff,nfu)
              call gradx(n,wa(nx1),bl,bu,wa(ngry),wa(ngr1),jbound)
      end if
c--------------------------------------------------------------------
c     Optimality test.
c---------------------------------------------------------------------
      irot=3
c---------------------------------------------------------------------
c     Decide if converged or if it necessary to continue
c--------------------------------------------------------------------
      kal=kal+1
      if(dabs(f1-fopt).ge.1.d-13*dmax1(1.d0,dabs(fopt)))then
              kal=0
              ierp=0
      else
              if(kal.ge.2)ierp=2
      end if

      ier=ierstf(n,bl,bu,wa(nx1),f1,wa(ngr1),wa(ngry),wa(nxy),eps,
     *           nfu,wa(naux1),fu,idiff,ibound,jbound)
      if(ier.eq.-2)k=kmax
      if(ier.le.-1)then
              if(ierp.eq.2.and.kal.gt.5)then
                      ier=2
                      go to 30
              end if
              irot=1
c----------------------------------------------------------------------
c     Decide if either update the Hessian or
c     recompute it.
c----------------------------------------------------------------------
              if(k.lt.kmax)then
                      k=k+1
                      call updaf(n,bl,bu,wa(nd),wa(ne),wa(nqt),wa(nsq),
     *                     x0,fu,ig,wa(ngr0),wa(ngr1),wa(naux1),ibound,
     *                     jbound,nfu,idiff)
                      irot=2
              end if
      end if
c----------------------------------------------------------------------
c     Restore the current iterate, its function value and
c     its numerical gradient.
c     If irot.le.2 continue
c     else --> return
c----------------------------------------------------------------------
30    fopt=f1

      do i=1,n
              x0(i)=wa(nmx1+i)
              wa(nmgr0+i)=wa(nmgr1+i)
      end do

      go to (10,20)irot
c----------------------------------------------------------------------
c     Restore the optimal point and the projected gradient
c     in the original variables before return.
c----------------------------------------------------------------------
40    if(ibound.ne.0)then
              do i= 1,n
                      x0(i)= wa(nmxy+i)
                      wa(nmgr0+i)=wa(naux1+i-1)
              end do
      end if
      return
      end
