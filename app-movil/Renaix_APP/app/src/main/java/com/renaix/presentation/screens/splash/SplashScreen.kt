package com.renaix.presentation.screens.splash

import androidx.compose.animation.core.*
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.renaix.R
import com.renaix.di.AppContainer
import com.renaix.presentation.common.components.ButterflyLoadingIndicator
import com.renaix.ui.theme.Purple300
import com.renaix.ui.theme.Purple500
import com.renaix.ui.theme.Purple700
import com.renaix.util.Constants
import kotlinx.coroutines.delay

/**
 * Pantalla de Splash con animaciones de mariposa
 * - Logo con efecto de aleteo sutil
 * - Entrada escalonada de elementos
 * - Indicador de carga personalizado
 */
@Composable
fun SplashScreen(
    appContainer: AppContainer,
    onNavigateToLogin: () -> Unit,
    onNavigateToMain: () -> Unit
) {
    val authRepository = appContainer.authRepository

    // Estados de animación escalonada
    var showLogo by remember { mutableStateOf(false) }
    var showTitle by remember { mutableStateOf(false) }
    var showSubtitle by remember { mutableStateOf(false) }
    var showLoader by remember { mutableStateOf(false) }

    // Animación de entrada del logo con spring
    val logoScale by animateFloatAsState(
        targetValue = if (showLogo) 1f else 0.3f,
        animationSpec = spring(
            dampingRatio = Spring.DampingRatioMediumBouncy,
            stiffness = Spring.StiffnessLow
        ),
        label = "logoScale"
    )
    val logoAlpha by animateFloatAsState(
        targetValue = if (showLogo) 1f else 0f,
        animationSpec = tween(durationMillis = 600),
        label = "logoAlpha"
    )

    // Animación de aleteo continuo de la mariposa
    val infiniteTransition = rememberInfiniteTransition(label = "butterflyWing")
    val wingRotation by infiniteTransition.animateFloat(
        initialValue = -3f,
        targetValue = 3f,
        animationSpec = infiniteRepeatable(
            animation = tween(800, easing = EaseInOutSine),
            repeatMode = RepeatMode.Reverse
        ),
        label = "wingRotation"
    )
    val wingScale by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = 1.02f,
        animationSpec = infiniteRepeatable(
            animation = tween(600, easing = EaseInOutSine),
            repeatMode = RepeatMode.Reverse
        ),
        label = "wingScale"
    )

    // Animaciones del título
    val titleAlpha by animateFloatAsState(
        targetValue = if (showTitle) 1f else 0f,
        animationSpec = tween(durationMillis = 500),
        label = "titleAlpha"
    )
    val titleOffset by animateFloatAsState(
        targetValue = if (showTitle) 0f else 30f,
        animationSpec = tween(durationMillis = 500, easing = EaseOutCubic),
        label = "titleOffset"
    )

    // Animaciones del subtítulo
    val subtitleAlpha by animateFloatAsState(
        targetValue = if (showSubtitle) 1f else 0f,
        animationSpec = tween(durationMillis = 500),
        label = "subtitleAlpha"
    )

    // Animación del loader
    val loaderAlpha by animateFloatAsState(
        targetValue = if (showLoader) 1f else 0f,
        animationSpec = tween(durationMillis = 400),
        label = "loaderAlpha"
    )

    // Secuencia de animaciones escalonadas
    LaunchedEffect(key1 = true) {
        showLogo = true
        delay(300)
        showTitle = true
        delay(200)
        showSubtitle = true
        delay(200)
        showLoader = true
        delay(Constants.SPLASH_DELAY_MILLIS - 700)

        // Verificar sesión
        if (authRepository.isSessionValid()) {
            onNavigateToMain()
        } else {
            onNavigateToLogin()
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                Brush.verticalGradient(
                    colors = listOf(
                        Purple700,
                        Purple500,
                        Purple300
                    )
                )
            )
            .semantics { contentDescription = "Pantalla de carga de Renaix" },
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
            modifier = Modifier.padding(horizontal = 32.dp)
        ) {
            // Logo de la mariposa con efecto de aleteo
            Image(
                painter = painterResource(id = R.drawable.ic_renaix_logo),
                contentDescription = "Logo de Renaix - Mariposa",
                modifier = Modifier
                    .size(200.dp)
                    .scale(logoScale)
                    .alpha(logoAlpha)
                    .graphicsLayer {
                        rotationZ = wingRotation
                        scaleX = wingScale
                        scaleY = wingScale
                    }
                    .padding(bottom = 24.dp),
                contentScale = ContentScale.Fit
            )

            // Nombre de la app con entrada desde abajo
            Text(
                text = "RENAIX",
                fontSize = 52.sp,
                fontWeight = FontWeight.Bold,
                color = Color.White,
                letterSpacing = 4.sp,
                modifier = Modifier
                    .alpha(titleAlpha)
                    .graphicsLayer { translationY = titleOffset }
            )

            Spacer(modifier = Modifier.height(12.dp))

            // Subtítulo con fade in
            Text(
                text = "Tu marketplace de segunda mano",
                style = MaterialTheme.typography.bodyLarge,
                color = Color.White.copy(alpha = 0.9f),
                modifier = Modifier.alpha(subtitleAlpha)
            )

            Spacer(modifier = Modifier.height(48.dp))

            // Indicador de carga personalizado con tema mariposa
            Box(modifier = Modifier.alpha(loaderAlpha)) {
                ButterflyLoadingIndicator(
                    modifier = Modifier.size(48.dp),
                    color = Color.White
                )
            }
        }
    }
}
