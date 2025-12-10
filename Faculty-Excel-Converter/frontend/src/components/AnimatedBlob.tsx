export function AnimatedBlob() {
  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
      {/* Center large blob */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
        <div className="blob-main"></div>
      </div>

      {/* Top left blob */}
      <div className="absolute top-20 left-20">
        <div className="blob-small blob-delay-1"></div>
      </div>

      {/* Top right blob */}
      <div className="absolute top-32 right-32">
        <div className="blob-medium blob-delay-2"></div>
      </div>

      {/* Bottom left blob */}
      <div className="absolute bottom-24 left-40">
        <div className="blob-medium blob-delay-3"></div>
      </div>

      {/* Bottom right blob */}
      <div className="absolute bottom-40 right-24">
        <div className="blob-small blob-delay-4"></div>
      </div>

      {/* Floating blob center-right */}
      <div className="absolute top-1/3 right-1/4">
        <div className="blob-small blob-delay-5"></div>
      </div>

      {/* Floating blob center-left */}
      <div className="absolute bottom-1/3 left-1/4">
        <div className="blob-small blob-delay-6"></div>
      </div>

      {/* Mid-top floating blob */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2">
        <div className="blob-tiny blob-delay-7"></div>
      </div>

      {/* Mid-bottom floating blob */}
      <div className="absolute bottom-1/4 left-1/3">
        <div className="blob-tiny blob-delay-8"></div>
      </div>

      <style>{`
        /* Main large blob - ULTRA CLEAR */
        .blob-main {
          width: 800px;
          height: 800px;
          border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%;
          background: radial-gradient(circle at 30% 30%,
            rgba(167, 139, 250, 0.95),
            rgba(139, 92, 246, 0.9),
            rgba(124, 58, 237, 0.85),
            rgba(109, 40, 217, 0.8)
          );
          filter: blur(20px) brightness(1.5) saturate(1.3);
          animation: blob-float-main 12s ease-in-out infinite;
          box-shadow:
            0 0 150px rgba(139, 92, 246, 0.9),
            0 0 250px rgba(168, 85, 247, 0.6),
            0 0 350px rgba(124, 58, 237, 0.4),
            inset 0 0 150px rgba(255, 255, 255, 0.2);
          will-change: transform, border-radius;
        }

        /* Medium blobs - HIGH CLARITY */
        .blob-medium {
          width: 500px;
          height: 500px;
          border-radius: 50% 60% 40% 70% / 60% 40% 70% 50%;
          background: radial-gradient(circle at 40% 40%,
            rgba(168, 85, 247, 0.9),
            rgba(147, 51, 234, 0.85),
            rgba(139, 92, 246, 0.8)
          );
          filter: blur(18px) brightness(1.6) saturate(1.4);
          animation: blob-float-medium 10s ease-in-out infinite;
          box-shadow:
            0 0 120px rgba(147, 51, 234, 0.8),
            0 0 200px rgba(168, 85, 247, 0.5),
            inset 0 0 100px rgba(255, 255, 255, 0.15);
          will-change: transform, border-radius;
        }

        /* Small blobs - CRYSTAL CLEAR */
        .blob-small {
          width: 350px;
          height: 350px;
          border-radius: 60% 40% 50% 70% / 50% 70% 40% 60%;
          background: radial-gradient(circle at 35% 35%,
            rgba(139, 92, 246, 0.92),
            rgba(124, 58, 237, 0.88),
            rgba(99, 102, 241, 0.84)
          );
          filter: blur(15px) brightness(1.7) saturate(1.5);
          animation: blob-float-small 8s ease-in-out infinite;
          box-shadow:
            0 0 100px rgba(99, 102, 241, 0.7),
            0 0 180px rgba(139, 92, 246, 0.5),
            inset 0 0 80px rgba(255, 255, 255, 0.18);
          will-change: transform, border-radius;
        }

        /* Tiny accent blobs - SUPER BRIGHT */
        .blob-tiny {
          width: 200px;
          height: 200px;
          border-radius: 45% 55% 60% 40% / 55% 45% 60% 40%;
          background: radial-gradient(circle at 50% 50%,
            rgba(196, 181, 253, 0.95),
            rgba(167, 139, 250, 0.9),
            rgba(139, 92, 246, 0.85)
          );
          filter: blur(12px) brightness(2) saturate(1.6);
          animation: blob-float-tiny 6s ease-in-out infinite;
          box-shadow:
            0 0 80px rgba(196, 181, 253, 0.8),
            0 0 140px rgba(167, 139, 250, 0.6),
            inset 0 0 60px rgba(255, 255, 255, 0.25);
          will-change: transform, border-radius;
        }

        /* Animation delays */
        .blob-delay-1 { animation-delay: 0s; }
        .blob-delay-2 { animation-delay: 1.2s; }
        .blob-delay-3 { animation-delay: 2.4s; }
        .blob-delay-4 { animation-delay: 3.6s; }
        .blob-delay-5 { animation-delay: 4.8s; }
        .blob-delay-6 { animation-delay: 6s; }
        .blob-delay-7 { animation-delay: 7.2s; }
        .blob-delay-8 { animation-delay: 8.4s; }

        /* Main blob animation - Enhanced */
        @keyframes blob-float-main {
          0%, 100% {
            border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%;
            transform: translate(0, 0) rotate(0deg) scale(1);
            filter: blur(20px) brightness(1.5) saturate(1.3);
          }
          25% {
            border-radius: 50% 60% 40% 70% / 60% 40% 70% 50%;
            transform: translate(-30px, -40px) rotate(90deg) scale(1.08);
            filter: blur(22px) brightness(1.6) saturate(1.4);
          }
          50% {
            border-radius: 60% 40% 50% 70% / 50% 70% 40% 60%;
            transform: translate(40px, -30px) rotate(180deg) scale(0.96);
            filter: blur(18px) brightness(1.55) saturate(1.35);
          }
          75% {
            border-radius: 70% 50% 60% 40% / 40% 60% 50% 70%;
            transform: translate(-40px, 30px) rotate(270deg) scale(1.04);
            filter: blur(21px) brightness(1.58) saturate(1.38);
          }
        }

        /* Medium blob animation - Enhanced */
        @keyframes blob-float-medium {
          0%, 100% {
            border-radius: 50% 60% 40% 70% / 60% 40% 70% 50%;
            transform: translate(0, 0) rotate(0deg) scale(1);
            filter: blur(18px) brightness(1.6) saturate(1.4);
          }
          33% {
            border-radius: 60% 40% 70% 50% / 50% 70% 40% 60%;
            transform: translate(50px, 40px) rotate(120deg) scale(1.12);
            filter: blur(20px) brightness(1.7) saturate(1.5);
          }
          66% {
            border-radius: 40% 70% 50% 60% / 70% 50% 60% 40%;
            transform: translate(-40px, -50px) rotate(240deg) scale(0.92);
            filter: blur(16px) brightness(1.65) saturate(1.45);
          }
        }

        /* Small blob animation - Enhanced */
        @keyframes blob-float-small {
          0%, 100% {
            border-radius: 60% 40% 50% 70% / 50% 70% 40% 60%;
            transform: translate(0, 0) rotate(0deg) scale(1);
            filter: blur(15px) brightness(1.7) saturate(1.5);
          }
          20% {
            border-radius: 40% 60% 70% 50% / 60% 50% 70% 40%;
            transform: translate(30px, -25px) rotate(72deg) scale(1.18);
            filter: blur(17px) brightness(1.8) saturate(1.6);
          }
          40% {
            border-radius: 70% 50% 40% 60% / 40% 70% 50% 60%;
            transform: translate(-25px, 35px) rotate(144deg) scale(0.88);
            filter: blur(13px) brightness(1.75) saturate(1.55);
          }
          60% {
            border-radius: 50% 70% 60% 40% / 70% 40% 60% 50%;
            transform: translate(35px, 30px) rotate(216deg) scale(1.08);
            filter: blur(16px) brightness(1.78) saturate(1.58);
          }
          80% {
            border-radius: 60% 50% 70% 40% / 50% 60% 40% 70%;
            transform: translate(-30px, -30px) rotate(288deg) scale(0.95);
            filter: blur(14px) brightness(1.73) saturate(1.53);
          }
        }

        /* Tiny blob animation - Enhanced */
        @keyframes blob-float-tiny {
          0%, 100% {
            border-radius: 45% 55% 60% 40% / 55% 45% 60% 40%;
            transform: translate(0, 0) rotate(0deg) scale(1);
            filter: blur(12px) brightness(2) saturate(1.6);
          }
          25% {
            border-radius: 55% 45% 40% 60% / 45% 55% 40% 60%;
            transform: translate(25px, -20px) rotate(90deg) scale(1.25);
            filter: blur(14px) brightness(2.2) saturate(1.7);
          }
          50% {
            border-radius: 60% 40% 55% 45% / 40% 60% 55% 45%;
            transform: translate(-20px, 25px) rotate(180deg) scale(0.85);
            filter: blur(10px) brightness(2.1) saturate(1.65);
          }
          75% {
            border-radius: 40% 60% 45% 55% / 60% 40% 45% 55%;
            transform: translate(20px, 20px) rotate(270deg) scale(1.1);
            filter: blur(13px) brightness(2.15) saturate(1.68);
          }
        }
      `}</style>
    </div>
  );
}
